import os
import sys
import ctypes
from time import sleep
from queue import Queue
from typing import List, Union
from threading import Thread, Event
from modeltasks.task import ModelTask
from modeltasks.util.task import ConditionalSemaphore
from modeltasks.scheduler.abstract import AbstractScheduler, JobPipeline


class ThreadsafePipeline(JobPipeline):
    """
    A threadsafe job pipeline using queues
    """
    
    _lock: ConditionalSemaphore = None
    
    @property
    def lock(self):
        return self._lock
    
    @lock.setter
    def lock(self, semaphore: ConditionalSemaphore):
        self._lock = semaphore
    
    def __init__(self):
        self._jobs = Queue()
        
    def _add_jobs(self, jobs: List):
        self._jobs.put(jobs)
        
    def _get_jobs(self) -> List:
        if not self._jobs.empty():
            return self._jobs.get(block=False)
        else:
            return []

    def __len__(self):
        return self._jobs.qsize()


class ThreadedScheduler(AbstractScheduler):
    """
    A scheduler using threads for the simultaneous execution of jobs.
    """
    
    _done: Event = None
    _max_threads: int = 0
    
    def __init__(self, *args, max_threads: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self._concurrent = kwargs.get('run_concurrent', True)
        self._max_threads = max_threads
        self._pending = Queue()
        self._done = Event()
    
    def run(self, use_cache: bool = None):
        """
        Execute the scheduled tasks (blocking until all tasks are done)
        """
        if use_cache is not None:
            self._use_cache = bool(use_cache)

        # Start the scheduler
        if not self._scheduler:
            self._scheduler = Thread(target=self._schedule_jobs)
        self._scheduler.start()
        
    def schedule(self, plan: List[List], pipeline: Union[int, str] = None) -> JobPipeline:
        pipeline = pipeline if pipeline is not None else 'default'
        pipeline = self._pipelines.setdefault(pipeline, ThreadsafePipeline())
        [pipeline.add(job) for job in plan]

        # Start worker for the pipeline
        max_concurrent = sum([p.concurrent_jobs for p in self.pipelines]) if self._concurrent else 1
        available_cpu = os.cpu_count() - 2 if os.cpu_count() > 3 else 1
        max_threads = min([self._max_threads, available_cpu]) if self._max_threads > 0 else available_cpu
        max_workers = min([max_concurrent, max_threads]) if self.concurrent else 1
        running_workers = len(self._workers)
        if (missing_workers := max_workers - running_workers) > 0:
            self._logger.debug(f'Invoking {missing_workers} worker threads to process task schedule')
            workers = [
                Thread(target=self._process_jobs, name=f'Worker {mw + running_workers + 1}', args=(mw + running_workers + 1,)) for mw in
                range(missing_workers)
            ]
            for w in workers:
                w.start()
            self._workers.extend(workers)

        return pipeline
                
    def _process_jobs(self, worker):
        self._logger.debug(f'Worker {worker} started')
        pending_jobs = self._pending
        while not self._done.is_set():
            job, lock = pending_jobs.get(block=True)

            def on_executed(task: ModelTask):
                # Release the aquired semaphore/lock again
                lock.release()

            def on_failed(task: ModelTask, error: Exception):
                # Set the done event
                self._done.set()

            if not self.execute_job(
                job,
                on_executed,
                on_failed,
                executor=f'Worker {worker}' if len(self._workers) > 1 else None
            ):
                break

        self._logger.debug(f'Worker {worker} exiting')
    
    def _schedule_jobs(self):
        # Set initial task counter state
        task_counter = sum([len(p) for p in self.pipelines])
        task_total = task_counter
        task_percentage = 0
        self._logger.debug(f'Scheduler: {task_counter} jobs to schedule (0% scheduled)')

        # Loop as long as we have no tasks left to schedule or if an error occured        
        while task_counter > 0 and not self._done.is_set():
            # Try to schedule
            for index, pipeline in self._pipelines.items():
                # Make sure the plan is locked by a conditional semaphore keeping track of all tasks being completed
                if not pipeline.paused and not pipeline.lock:
                    jobs = pipeline.get()
                    pipeline.lock = ConditionalSemaphore(max_slots=len(jobs))
                    for i, j in enumerate(jobs):
                        self._logger.debug(f'Scheduler: Scheduling {str(i + 1) + " of " + str(len(jobs)) + " concurrent tasks" if len(jobs) > 1 else "one task"} from job pipeline {index if len(self.pipelines) > 1 else ""}')
                        pipeline.lock.acquire()
                        self._pending.put(
                            (
                                j,
                                pipeline.lock
                            )
                        )
                if pipeline.lock and pipeline.lock.is_reset():
                    pipeline.lock = None
            sleep(0.1)
            
            # Update the task counter
            current_percentage = 100 - int(task_counter / task_total * 100)
            if current_percentage != task_percentage:
                task_percentage = current_percentage
                self._logger.debug(f'Scheduler: {task_counter} jobs remaining ({current_percentage}% scheduled)')
            task_counter = sum([len(p) for p in self.pipelines])

        # We quit the loop: See why (success or failure?)
        if self._done.is_set():
            # Put False jobs to make workers quit
            [self._pending.put((False, False)) for _ in range(len(self._workers))]
            sleep(1)
            # Clear pipeline
            with self._pending.mutex:
                self._pending.queue.clear()
            # Try last attempt to stop threads
            try:
                for worker in [w for w in self._workers if w.is_alive()]:
                    self._logger.info(f'Model failed: Trying to cancel active {worker.name.lower()}')
                    exc = ctypes.py_object(SystemExit)
                    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(worker.ident), exc)
                    if res == 0:
                        raise ValueError("Nonexistant Thread ID")
                    elif res > 1:
                        ctypes.pythonapi.PyThreadState_SetAsyncExc(worker.ident, None)
                        raise SystemError("Failed to set thread async state")
            finally:
                sleep(1)
                self._logger.error(f'Failed to execute model!')
                sys.exit()
        else:
            self._logger.debug(f'Scheduler: {task_counter} jobs remaining (100% scheduled, {self._pending.qsize()} tasks still awaiting to be processed)')
            # Put "False" jobs to make workers quit (Workers quit if they receive False from the pending job queue)
            [self._pending.put((False, False)) for _ in range(len(self._workers))]

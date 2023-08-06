import logging
import time
from functools import wraps
from typing import Callable

default_logger = logging.getLogger(__name__)


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(
        self,
        logger: Callable = default_logger.info,
        log_message: str = "Elapsed time: {:0.4f} seconds",
    ) -> None:
        self.logger = logger
        self.text: str = log_message
        self._start_time = None

    def start(self) -> None:
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if self.logger:
            self.logger(self.text.format(elapsed_time))

        return elapsed_time

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()


class StepTimer(Timer):
    def __init__(
        self,
        *,
        logger: Callable = default_logger.info,
        print_start: bool = False,
        **kwargs,
    ):
        self.before_print = print_start
        super().__init__(logger=logger, **kwargs)

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if self.before_print:
                self.logger(f"Starting execution of function {func.__name__}")
            with self:
                result = func(*args, **kwargs)
            return result

        return wrapped_func

import logging
import time
from typing import List, Type, Union
from functools import wraps

default_logger = logging.getLogger(__name__)
Numeric = Union[int, float]


class Retry:
    def __init__(
        self,
        *,
        n_retries: int,
        retry_on_error: Union[Type[Exception], List[Type[Exception]]] = Exception,
        wait_between_tries: Numeric = 0,
    ) -> None:
        self.logger = default_logger
        self.n_retries = n_retries
        self.retry_on_error = (
            retry_on_error if isinstance(retry_on_error, list) else [retry_on_error]
        )
        self.wait_between_tries = wait_between_tries

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            for attempt in range(self.n_retries):
                self.logger.info(
                    f"Starting attempt #{attempt +1} of function {func.__name__}"
                )
                try:
                    result = func(*args, **kwargs)
                    break
                except (err for err in self.retry_on_error) as e:
                    self.logger.info(
                        f"Failed executing {func.__name__} due to exception: {e}"
                    )
                    time.sleep(self.wait_between_tries)

            return result

        return wrapped_func

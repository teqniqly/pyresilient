import functools
from abc import ABC, abstractmethod
from logging import Logger


class RetryStrategyBase(ABC):
    @abstractmethod
    def __init__(self, logger: Logger):
        self._logger = logger

    @abstractmethod
    def retry(self):
        pass


# noinspection PyBroadException
class RetryStrategy(RetryStrategyBase):
    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    def retry(self, max_retries=1):
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1.")

        def retry_wrapper(func):
            @functools.wraps(func)
            def execute(*args, **kwargs):
                current_try = 0
                while current_try < max_retries:
                    try:
                        return func(*args, **kwargs)
                    except Exception:
                        current_try += 1

                        if current_try == max_retries:
                            raise

            return execute

        return retry_wrapper

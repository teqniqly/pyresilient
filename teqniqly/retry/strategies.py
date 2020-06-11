import functools
import time
from abc import ABC, abstractmethod
from logging import Logger


# noinspection PyBroadException
class RetryStrategyBase(ABC):
    @abstractmethod
    def __init__(self, logger: Logger):
        self._logger = logger
        self._retry_args = []
        self._retry_kwargs = {}

    @abstractmethod
    def pre_execute(self, *args, **kwargs):
        pass

    @abstractmethod
    def post_retry(self):
        pass

    def retry(self, *args, **kwargs):
        self._retry_args = args
        self._retry_kwargs = kwargs

        self.pre_execute()

        def retry_wrapper(func):
            @functools.wraps(func)
            def execute(*exec_args, **exec_kwargs):
                current_try = 0
                while current_try < int(self._retry_kwargs.get("max_retries")):
                    try:
                        return func(*exec_args, **exec_kwargs)
                    except Exception:
                        current_try += 1
                        self.post_retry()
                        if current_try == int(self._retry_kwargs.get("max_retries")):
                            raise

            return execute

        return retry_wrapper


class RetryStrategy(RetryStrategyBase):
    def __init__(self, logger: Logger):
        super().__init__(logger=logger)
        self._max_retries = None

    def pre_execute(self):
        max_retries = int(self._retry_kwargs.get("max_retries"))
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1.")

    def post_retry(self):
        pass


class RetryWithFixedDelayStrategy(RetryStrategy):
    def __init__(self, logger: Logger):
        super().__init__(logger)
        self._delay = None

    def pre_execute(self):
        self._delay = int(self._retry_kwargs.get("delay"))

        if self._delay < 1:
            raise ValueError("delay must be at least one second.")

        super().pre_execute()

    def post_retry(self):
        time.sleep(self._delay)
        super().post_retry()

import functools
import time
from abc import ABC, abstractmethod
from logging import Logger


# noinspection PyBroadException
from typing import Generator


class RetryStrategyBase(ABC):
    @abstractmethod
    def __init__(self, logger: Logger = None):
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
    def __init__(self, logger: Logger = None):
        super().__init__(logger=logger)
        self._max_retries = None

    def pre_execute(self):
        self._max_retries = self._retry_kwargs.get("max_retries")

        if not self._max_retries:
            raise ValueError("A max_retries value of at least 1 must be specified.")

        if not isinstance(self._max_retries, int):
            raise ValueError(
                "The max_retries value must be an integer with a value of at least one."
            )

        if self._max_retries < 1:
            raise ValueError("The max_retries value must be at least 1.")

    def post_retry(self):
        pass


class RetryWithFixedDelayStrategy(RetryStrategy):
    def __init__(self, logger: Logger = None):
        super().__init__(logger)
        self._delay = None

    def pre_execute(self):
        self._delay = self._retry_kwargs.get("delay")

        if not self._delay:
            raise ValueError("A delay value of at least 1 second must be specified.")

        if not isinstance(self._delay, int):
            raise ValueError(
                "The delay value must be an integer with a value of at least one."
            )

        if self._delay < 1:
            raise ValueError("The delay value must be at least one second.")

        super().pre_execute()

    def post_retry(self):
        time.sleep(self._delay)
        super().post_retry()


class RetryWithVariableDelayStrategy(RetryStrategy):
    def __init__(self, logger: Logger = None):
        super().__init__(logger)
        self._delay_generator = None

    def pre_execute(self):
        self._delay_generator = self._retry_kwargs.get("delay_generator")

        if not self._delay_generator:
            raise ValueError("A delay_generator must be specified.")

        if not isinstance(self._delay_generator, Generator):
            raise ValueError("The delay_generator value must be a generator type.")

        super().pre_execute()

    def post_retry(self):
        time.sleep(next(self._delay_generator))
        super().post_retry()

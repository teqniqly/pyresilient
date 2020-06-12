"""
The Retry strategies module.
"""
import functools
import time
import teqniqly.utils.guards as guards

from abc import ABC, abstractmethod
from logging import Logger

# noinspection PyBroadException
from typing import Generator


class RetryStrategyBase(ABC):
    """
    The base class for retry strategies.
    """

    @abstractmethod
    def __init__(self, logger: Logger = None):
        """
        Base class initializer.
        :param logger: The logger.
        """
        self._logger = logger
        self._retry_args = []
        self._retry_kwargs = {}
        self._max_retries = None

    @abstractmethod
    def pre_execute(self):
        """
        Specifies the logic to run before the wrapped method executes.
        """
        self._max_retries = self._retry_kwargs.get("max_retries")
        guards.assert_type(self._max_retries, int)
        guards.assert_true(self._max_retries > 0)

    @abstractmethod
    def post_retry(self):
        """
        Specifies the logic to run after the wrapped method fails.
        """
        pass

    def retry(self, *args, **kwargs):
        """
        The retry decorator. When all retries are exhausted the last exception is re-raised.
        Args:
            *args: Decorator arguments. These are specific to derived classes.
            **kwargs: Decorator keyword arguments. These are specific to derived classes.

        Returns:
        The decorated function.
        """
        self._retry_args = args
        self._retry_kwargs = kwargs

        self.pre_execute()

        def retry_wrapper(func):
            # noinspection PyBroadException
            @functools.wraps(func)
            def execute(*exec_args, **exec_kwargs):
                current_try = 0
                while current_try < self._max_retries:
                    try:
                        return func(*exec_args, **exec_kwargs)
                    except Exception:
                        current_try += 1
                        self.post_retry()
                        if current_try == self._max_retries:
                            raise

            return execute

        return retry_wrapper


class RetryStrategy(RetryStrategyBase):
    """
    Specifies a simple retry strategy, i.e. retry a specific number of times without a delay.
    """

    def __init__(self, logger: Logger = None):
        """
        Initializes a RetryStrategy instance.
        Args:
            logger: The logger.
        """
        super().__init__(logger=logger)
        self._max_retries = None

    def pre_execute(self):
        """
        Specifies the logic to run before the wrapped method executes.
        """
        super().pre_execute()

    def post_retry(self):
        """
        Specifies the logic to run after the wrapped method fails.
        """
        super().post_retry()


class RetryWithFixedDelayStrategy(RetryStrategy):
    """
    Specifies a retry strategy where the failing operation is retried a specific number of times
    with a fixed delay in between retries.

    The retry decorator must called with the following keyword args:
        - delay: The delay in seconds.
        - max_retries: The maximum number of retries.
    """

    def __init__(self, logger: Logger = None):
        """
        Initializes a RetryWithFixedDelayStrategy instance.
        Args:
            logger: The logger.
        """
        super().__init__(logger)
        self._delay = None

    def pre_execute(self):
        """
        Specifies the logic to run before the wrapped method executes.
        """
        self._delay = self._retry_kwargs.get("delay")
        guards.assert_type(self._delay, int)
        guards.assert_true(self._delay > 1)
        super().pre_execute()

    def post_retry(self):
        """
        Specifies the logic to run after the wrapped method fails.
        """
        time.sleep(self._delay)
        super().post_retry()


class RetryWithVariableDelayStrategy(RetryStrategy):
    """
    Specifies a retry strategy where the failing operation is retried a specific number of times
    with a variable delay in between retries. The variable delay is specified via a Generator.

    The retry decorator must called with the following keyword args:
        - delay_generator: A generator providing the retry delays in seconds. The values provided by the generator should be
          equal to or greater than the number of retries.

        - max_retries: The maximum number of retries.
    """

    def __init__(self, logger: Logger = None):
        """
        Initializes a RetryWithFixedDelayStrategy instance.
        Args:
            logger: The logger.
        """
        super().__init__(logger)
        self._delay_generator = None

    def pre_execute(self):
        """
        Specifies the logic to run before the wrapped method executes.
        """
        self._delay_generator = self._retry_kwargs.get("delay_generator")
        guards.assert_type(self._delay_generator, Generator)
        super().pre_execute()

    def post_retry(self):
        """
        Specifies the logic to run after the wrapped method fails.
        """
        time.sleep(next(self._delay_generator))
        super().post_retry()

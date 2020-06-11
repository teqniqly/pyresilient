import time
from logging import Logger
from unittest import TestCase

from teqniqly.retry.strategies import RetryStrategy, RetryWithFixedDelayStrategy

logger = Logger(__name__)
simple_strategy = RetryStrategy(logger)
fixed_delay_strategy = RetryWithFixedDelayStrategy(logger)


class TestClass:
    def __init__(self, succeed_after_n_retries: int):
        self._succeed_after_n_retries = succeed_after_n_retries
        self.retry_count = 0

    def _execute(self, return_value: int = 0) -> int:
        try:
            if self.retry_count < self._succeed_after_n_retries:
                raise ValueError("Oops!")

            return return_value
        except:
            self.retry_count += 1
            raise

    @simple_strategy.retry(max_retries=10)
    def execute_retry_simple(self, return_value: int = 0) -> int:
        return self._execute(return_value)

    @fixed_delay_strategy.retry(delay=2, max_retries=10)
    def execute_retry_with_delay(self, return_value: int = 0) -> int:
        return self._execute(return_value)


class RetryStrategyTests(TestCase):
    def test_retry_strategy(self):
        # Arrange
        tc = TestClass(3)

        # Act
        result = tc.execute_retry_simple(10)

        # Assert
        self.assertEqual(3, tc.retry_count)
        self.assertEqual(10, result)

    def test_when_retries_exhausted_raises_original_Exception(self):
        # Arrange
        tc = TestClass(12)

        # Act, Assert
        with self.assertRaises(ValueError):
            tc.execute_retry_simple()


class RetryWithFixedDelayStrategy(TestCase):
    def test_retry_strategy(self):
        # Arrange
        tc = TestClass(3)

        # Act
        start_time = time.time()
        result = tc.execute_retry_with_delay(10)
        end_time = time.time() - start_time

        # Assert
        self.assertEqual(3, tc.retry_count)
        self.assertEqual(10, result)
        self.assertAlmostEqual(end_time, 6, places=2)

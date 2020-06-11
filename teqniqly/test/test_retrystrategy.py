from logging import Logger
from unittest import TestCase
from unittest.mock import MagicMock

from teqniqly.retry.strategies import RetryStrategy

strategy = RetryStrategy(Logger(__name__))


class TestClass:
    def __init__(self, succeed_after_n_retries: int):
        self._succeed_after_n_retries = succeed_after_n_retries
        self.retry_count = 0

    @strategy.retry(max_retries=10)
    def execute(self, return_value: int = 0) -> int:
        try:
            if self.retry_count < self._succeed_after_n_retries:
                raise ValueError("Oops!")

            return return_value
        except:
            self.retry_count += 1
            raise


class RetryStrategyTests(TestCase):
    def test_retry_strategy(self):
        # Arrange
        tc = TestClass(3)

        # Act
        result = tc.execute(10)

        # Assert
        self.assertEqual(3, tc.retry_count)
        self.assertEqual(10, result)

    def test_when_retries_exhausted_raises_original_Exception(self):
        # Arrange
        tc = TestClass(12)

        # Act, Assert
        with self.assertRaises(ValueError):
            tc.execute()

from unittest import TestCase

from teqniqly.retry.strategies import (
    RetryStrategy,
    RetryWithFixedDelayStrategy,
    RetryWithVariableDelayStrategy,
)


class RetryStrategyErrorTests(TestCase):
    def func(self):
        pass

    def test_when_max_retries_not_valid_raise_ValueError(self):
        # Arrange
        strategy = RetryStrategy()
        invalid_values = [None, 0, -1, "foobar"]

        # Act, Assert
        for i in invalid_values:
            with self.assertRaises(ValueError):
                strategy.retry(max_retries=i)(self.func)


class RetryWithFixedDelayStrategyErrorTests(TestCase):
    def func(self):
        pass

    def test_when_max_retries_not_valid_raise_ValueError(self):
        # Arrange
        strategy = RetryWithFixedDelayStrategy()
        invalid_values = [None, 0, -1, "foobar"]

        # Act, Assert
        for i in invalid_values:
            with self.assertRaises(ValueError):
                strategy.retry(max_retries=i)(self.func)

    def test_when_delay_not_valid_raise_ValueError(self):
        # Arrange
        strategy = RetryWithFixedDelayStrategy()
        invalid_values = [None, 0, -1, "foobar"]

        # Act, Assert
        for i in invalid_values:
            with self.assertRaises(ValueError):
                strategy.retry(max_retries=10, delay=i)(self.func)


class RetryWithVariableDelayStrategyErrorTests(TestCase):
    def func(self):
        pass

    def test_when_max_retries_not_valid_raise_ValueError(self):
        # Arrange
        strategy = RetryWithVariableDelayStrategy()
        invalid_values = [None, 0, -1, "foobar"]

        # Act, Assert
        for i in invalid_values:
            with self.assertRaises(ValueError):
                strategy.retry(max_retries=i)(self.func)

    def test_when_delay_generator_not_valid_raise_ValueError(self):
        # Arrange
        strategy = RetryWithVariableDelayStrategy()
        invalid_values = [None, "foo", range(1, 100)]

        # Act, Assert
        for i in invalid_values:
            with self.assertRaises(ValueError):
                strategy.retry(max_retries=10, delay_generator=i)(self.func)

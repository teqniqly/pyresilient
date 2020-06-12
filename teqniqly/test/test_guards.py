from functools import partial

import teqniqly.utils.guards as guards
from unittest import TestCase


class GuardsTests(TestCase):
    def test_assert_scalar_raises_ValueError(self):
        # Arrange
        invalid_values = ["foobar", 10.0, int, []]

        # Act, Assert
        for i in invalid_values:
            with self.assertRaises(ValueError):
                guards.assert_type(i, int)

    def test_assert_true_raises_ValueError(self):
        # Arrange
        def predicate(x: int) -> bool:
            return x % 2 == 0

        # Act
        with self.assertRaises(ValueError):
            guards.assert_true(predicate(11))

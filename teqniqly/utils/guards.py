from typing import Type


def assert_type(val, expected_type: Type):
    if not val:
        raise ValueError(
            "assert_type expects a parameter 'val' which was not supplied."
        )

    if not expected_type:
        raise ValueError(
            "assert_scalar expects a parameter 'expected_type' which was not supplied."
        )

    if isinstance(val, expected_type):
        return

    raise ValueError(
        f"Invalid type for parameter. Expected a type of {expected_type} but got {type(val)}."
    )


def assert_true(predicate):

    if predicate is None:
        raise ValueError("assert_true expects a 'predicate' which was not supplied.")

    if not predicate:
        raise ValueError("assert_true returned False for the given predicate.")

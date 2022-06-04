"""
---- pytest check ----
"""


def multiply_by_two(num):
    """
    sample function to test by pytest
    """
    return num * 2


def test_multiply_by_two():
    """
    test function
    """
    assert multiply_by_two(4) == 8

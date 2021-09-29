"""
Examples of tests using pytest.
Read these functions and then fix the TODOs in the end of the file.
You can learn about pytest here:
https://www.guru99.com/pytest-tutorial.html
"""
import random
from typing import Union
from typing import List
import numpy as np
import pandas as pd
import string

import pytest


def test_simple_test():
    assert 1 > 0
    assert len("123456") == 6
    assert 2 > 1 * 1.5, "This will be print if the test fails"


def fibonacci(n: int) -> int:
    """
    Will return the Fn element of fibonacci series
    Args:
        n: The element index

    Returns:
        The n'th fibonacci number
    """
    if n < 2:
        return 1
    fn = 1
    fn_minus_1 = 1
    for i in range(2, n + 1):
        next_item = fn + fn_minus_1
        fn_minus_1 = fn
        fn = next_item
    return fn


# Test the function using parametrize. Give few examples of index and the fibonacci element in that index.
# learn more about parametrize here: https://www.guru99.com/pytest-tutorial.html#11
@pytest.mark.parametrize("item_index, fibonacci_value", [(0, 1), (1, 1), (2, 2), (4, 5), (6, 13), (8, 34)])
def test_fibonacci_using_parametrize(item_index, fibonacci_value):
    assert fibonacci(item_index) == fibonacci_value


# Test the function using fixture.
# learn more about fixture here: https://www.guru99.com/pytest-tutorial.html#10


@pytest.fixture
def first_fibonacci_numbers():
    """
    This fixture is the first elements of the fibonacci series.
    (In real life this better be a constant, we use fixture for generating objects we need for testing)
    """
    return [1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_fibonacci_using_fixture(first_fibonacci_numbers):
    """
    Test the fibonacci function. Tests the first elements of the series.
    Args:
        first_fibonacci_numbers: This is a fixture so it is automatically filled.
            The first_fibonacci_numbers will have the first elements of the fibonacci series
            see first_fibonacci_numbers() function.
    """
    for item_index, fibonacci_value in enumerate(first_fibonacci_numbers):
        assert fibonacci(item_index) == fibonacci_value


# TODO test this function, make sure for example please_test_me("testing is great") = "testing is great!!!"
def please_test_me(string: str) -> str:
    return string + "!!!"

def test_please_test_me():
    assert please_test_me("testing is great") == "testing is great!!!", "error"


def times_7(number: Union[int, float]):
    return number * 7


# TODO make_me_2_functions_one_use_fixture_and_one_use_parametrize
@pytest.mark.parametrize("num, res", [(0, 0), (2, 14), (4, 28), (-1, -7), (0.5, 3.5)])
def test_times_7_using_parametrize(num, res):
    assert times_7(num) == res


@pytest.fixture
def times_7_rnd_int():
    return random.Random().randint(-1000, 1000)


def test_times_7_using_fixture(times_7_rnd_int):
    assert times_7(times_7_rnd_int) == sum([times_7_rnd_int for i in range(7)])


def test_make_me_2_functions_one_use_fixture_and_one_use_parametrize():
    assert times_7(2) == 14
    assert times_7(4) == 28
    assert times_7(0) == 0
    assert times_7(-1) == -7
    assert times_7(0.5) == 3.5
    # TODO add one interesting case I didn't check

    random_generator = random.Random()
    for i in range(10):
        rnd_int = random_generator.randint(-1000, 1000)
        # time_7(rnd_int) is like summing 7 items of rnd_int
        assert times_7(rnd_int) == sum([rnd_int for i in range(7)])

        # assert times_7(rnd_int) > rnd_int  # TODO Explain why this assert doest work -
        #  because rnd_int can be negative number therefore it is not true.


# TODO Add a function and at least 3 tests
def add_10(number: Union[int, float]):
    return number+10


@pytest.mark.parametrize("num, res", [(0, 10), (2, 12), (-10, 0), (-1, 9), (0.5, 10.5)])
def test_add_10_using_parametrize(num, res):
    assert add_10(num) == res


@pytest.fixture
def add_10_rnd_int():
    return [10,11,12,13]


def test_add_10_using_fixture(add_10_rnd_int):
    for item_index, value in enumerate(add_10_rnd_int):
        assert add_10(item_index) == value


def test_add_10():
    assert add_10(-50) == -40


# TODO add a function that get data frame as an argument and return it after some preprocess/change
def add_prefix(df):
    df = df.add_prefix('col_')
    return df


# TODO test the function you wrote use assert_frame_equal and assert_series_equal
def test_add_prefix():
    df = pd.DataFrame({'a':[1,2,3],'b':[2,3,4]})
    output = pd.DataFrame({'col_a':[1,2,3],'col_b':[2,3,4]})
    res = add_prefix(df)
    pd.testing.assert_frame_equal(res,output)
    pd.testing.assert_series_equal(res['col_a'], output['col_a'])



def compute_weighted_average(x: List[float], w: List[float]) -> float:
    return sum([x1 * w1 for x1, w1 in zip(x, w)]) / sum(w)


def test_weighted_average_raise_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        assert compute_weighted_average([1, 0 ,1], [1, -1, 0])
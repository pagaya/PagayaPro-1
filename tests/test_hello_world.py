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
import pytest
import pandas as pd


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
    assert please_test_me("testing is great") == "testing is great!!!"


def times_7(number: Union[int, float]):
    return number * 7


# TODO make_me_2_functions_one_use_fixture_and_one_use_parametrize
def test_make_me_2_functions_one_use_fixture_and_one_use_parametrize():
    assert times_7(2) == 14
    assert times_7(4) == 28
    assert times_7(0) == 0
    assert times_7(-1) == -7
    # TODO add one interesting case I didn't check

    random_generator = random.Random()
    for i in range(10):
        rnd_int = random_generator.randint(-1000, 1000)
        # time_7(rnd_int) is like summing 7 items of rnd_int
        assert times_7(rnd_int) == sum([rnd_int for i in range(7)])

        # assert times_7(rnd_int) > rnd_int  # TODO Explain why this assert doest work
        # in case of rnd_int=0, times_7(0) = 0*7 = 0


@pytest.mark.parametrize("number, value", [(2, 14), (4, 28), (0, 0), (-1, -7), (np.inf, np.inf)])
def test_1_times_7(number, value):
    assert times_7(number) == value


@pytest.fixture
def random_generator():
    return random.Random()


def test_2_times_7(random_generator):
    for i in range(10):
        rnd_int = random_generator.randint(-1000, 1000)
        assert times_7(rnd_int) == sum([rnd_int for _ in range(7)])

# TODO Add a function and at least 3 tests
def factorial(n):
    fact = 1
    for i in range(1, n+1):
        fact *= i
    return fact


@pytest.mark.parametrize("number, value", [(0, 1), (1, 1), (3, 6), (8, 40320), (11, 39916800)])
def test_1_factorial(number, value):
    assert factorial(number) == value


def test_2_factorial(random_generator):
    for i in range(10):
        rnd_int = random_generator.randint(0, 1000)
        assert factorial(rnd_int) == factorial(rnd_int-1)*rnd_int


def test_3_factorial(random_generator):
    for i in range(10):
        rnd_int = random_generator.randint(4, 1000)
        assert factorial(rnd_int) > 2**rnd_int

# TODO add a function that get data frame as an argument and return it after some preprocess/change
# TODO test the function you wrote use assert_frame_equal and assert_series_equal
def same_func(df, col_name):
    return df.groupby(col_name).mean()#.reset_index()


@pytest.fixture
def get_df():
    df = pd.DataFrame(
        {

            "C": pd.Series(list(range(6)), dtype="float32"),
            "D": np.array([3] * 6, dtype="float32"),
            "E": pd.Categorical(["test", "train", "test", "train", "test", "train"]),
        }
    )
    return df


def test_same_func(get_df):
    s = pd.Series(data={'test': 2, 'train': 3}, index=pd.Index(pd.Categorical(["test", "train"])), dtype="float32",
                  name='C')
    s.index.set_names('E', inplace=True)
    df = pd.DataFrame(
        {
            "C": pd.Series([2, 3], dtype="float32"),
            "D": np.array([3] * 2, dtype="float32"),
            "E": pd.Categorical(["test", "train"]),
        }
    )
    df.set_index("E", inplace=True)

    pd.testing.assert_frame_equal(same_func(get_df, "E"), df)
    pd.testing.assert_series_equal(same_func(get_df, "E")["C"], s)


def compute_weighted_average(x: List[float], w: List[float]) -> float:
    return sum([x1 * w1 for x1, w1 in zip(x, w)]) / sum(w)


def test_weighted_average_raise_zero_division_error():
    # TODO check that weighted_average raise zero division error when the sum of the weights is 0
    with pytest.raises(ZeroDivisionError):
        assert compute_weighted_average([1, 2, 3], [-1, 0, 1])
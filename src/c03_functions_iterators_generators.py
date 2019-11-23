#!/usr/bin/env pytest-3

"""
Functions, Iterators, and Generators

This chapter will present several Python features from a functional viewpoint, as follows:
- Pure functions, free of side effects
- Functions as objects that can be passed as arguments or returned as results
- The use of Python strings using object-oriented suffix notation and prefix notation
- Using tuples and named tuples as a way to create stateless objects
- Using iterable collections as our primary design tool for functional programming
"""

import pathlib
from typing import Callable, TextIO

# pylint:disable=missing-docstring

# Writing pure functions

# A function with no side effects fits the pure mathematical abstraction of a function: there are
# no global changes to variables. Avoid the global statement. To be pure, a function should also
# avoid changing the state mutable objects.


def test_file_no_with() -> None:
    path = pathlib.Path("c03_file.txt")
    if path.is_file():
        path.unlink()

    file_write = path.open("w")
    try:
        file_write.write("hello world")
    finally:
        file_write.close()

    file_read = path.open("r")
    try:
        assert file_read.readline() == "hello world"
    finally:
        file_read.close()


def test_file_with() -> None:
    """
    We can't easily eliminate all stateful Python objects. We should always use the with statement
    to encapsulate stateful file objects into a well-defined scope. Files should be proper
    parameters to functions, and the open files should be nested in a with statement to assure that
    their stateful behavior is handled properly.

    This design pattern also applies to databases. A database connection object should generally be
    provided as a formal argument to an application's functions.
    """
    def write_message(file: TextIO, message: str) -> None:
        file.write(message)

    def read_message(file: TextIO) -> str:
        return file.readline()

    path = pathlib.Path("c03_file.txt")
    if path.is_file():
        path.unlink()

    with path.open("w") as file:
        write_message(file, "hello world")

    with path.open("r") as file:
        assert read_message(file)


# Functions as first-class objects


def test_callable_strategy() -> None:
    """
    We can assign functions to variables, pass functions as arguments, and return functions as
    values. We can easily use these techniques to write higher-order functions.

    Additionally, a callable object helps us to create functions. We can consider the callable
    class definition as a higher-order function. We do need to be judicious in how we use the
    __init__() method of a callable object; we should avoid setting stateful class variables. One
    common application is to use an __init__() method to create objects that fit the Strategy
    design pattern.
    """
    # pylint: disable=too-few-public-methods
    class Mersenne:
        def __init__(self, algorithm: Callable[[int], int]) -> None:
            self.pow2 = algorithm

        def __call__(self, arg: int) -> int:
            return self.pow2(arg) - 1

    def shifty(power: int) -> int:
        return 1 << power

    def multy(power: int) -> int:
        if power == 0:
            return 1
        return 2 * multy(power - 1)

    def faster(power: int) -> int:
        if power == 0:
            return 1
        if power % 2 == 1:
            return 2 * faster(power - 1)
        tmp_result = faster(power // 2)
        return tmp_result * tmp_result

    assert Mersenne(shifty)(4) == 15
    assert Mersenne(multy)(4) == 15
    assert Mersenne(faster)(4) == 15

# Using strings


def test_string_prefix_postfix() -> None:
    """
    Since Python strings are immutable, they're an excellent example of functional programming
    objects. A Python str object has a number of methods, all of which produce a new string as the
    result. These methods are pure functions with no side effects.

    The syntax for str method functions is postfix, where most functions are prefix. This means
    that complex string operations can be hard to read when they're co-mingled with conventional
    functions. For example, in this expression, len(variable.title()), the title() method is in
    postfix notation and the len() function is in prefix notation.
    """
    # Postfix
    money_amount = "£1,000"
    assert money_amount.replace("£", "").replace(",", "") == "1000"

    # Prefix
    def remove(string: str, chars: str) -> str:
        if chars:
            return remove(string.replace(chars[0], ""), chars[1:])
        return string

    assert remove(money_amount, "£,") == "1000"

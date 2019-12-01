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

import math
import pathlib
import itertools
from typing import Callable, TextIO, Tuple, NamedTuple, Iterator, Iterable, Any
from collections import namedtuple
import pytest

# pylint:disable=missing-docstring

# Writing pure functions


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
    A function with no side effects fits the pure mathematical abstraction of a function: there are
    no global changes to variables. Avoid the global statement. To be pure, a function should also
    avoid changing the state mutable objects.

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

# Using tuples and named tuples


def test_tuple_lambda() -> None:
    """
    Since Python tuples are immutable objects, they're another excellent example of objects
    suitable for functional programming.

    Consider working with a sequence of color values as a three tuple of the form (number, number,
    number). It's not clear that these are in red, green, blue order. We can clarify the triple
    structure by creating functions to pick a three-tuple apart. We can use red(item) to select the
    item that has the red component. It can help to provide a more formal type hint on each
    variable. For example, we can define a new type, RGB, as a three-tuple. The red variable is
    provided with a type hint of Callable[[RGB], int] to indicate it should be considered to be a
    function that accepts an RGB argument and produces an integer result.
    """
    RGB = Tuple[int, int, int]
    red: Callable[[RGB], int] = lambda colour: colour[0]
    green: Callable[[RGB], int] = lambda colour: colour[1]
    blue: Callable[[RGB], int] = lambda colour: colour[2]

    orange: RGB = (255, 165, 0)
    assert red(orange) == 255
    assert green(orange) == 165
    assert blue(orange) == 0


def test_tuple_namedtuple() -> None:
    Colour = namedtuple("Colour", ("red", "green", "blue", "name"))
    orange = Colour(255, 165, 0, "orange")
    assert orange.red == 255
    assert orange.green == 165
    assert orange.blue == 0
    assert orange.name == "orange"


def test_tuple_namedtuple_typed() -> None:
    """
    This definition of the Colour class defines a tuple with specific names and type hints for each
    position within the tuple. This preserves the advantages of performance and immutability. It
    adds the ability for the mypy program to confirm that the tuple is used properly.
    """
    class Colour(NamedTuple):
        """An RGB colour"""
        red: int
        green: int
        blue: int
        name: str

        def __repr__(self) -> str:
            return f"<Colour {self.name} red={self.red}, green={self.green}, blue={self.blue}>"

    orange = Colour(255, 165, 0, "orange")
    assert orange.red == 255
    assert orange.green == 165
    assert orange.blue == 0
    assert orange.name == "orange"
    assert repr(orange) == "<Colour orange red=255, green=165, blue=0>"

# Using generator expressions


def test_generator_function_tail_call_optimisation() -> None:
    """
    A generator expression is lazy and creates objects only as required. This can improve
    performance, unlike a list display (or comprehension) that can create a (potentially large)
    collection of objects. Caveat: Generators can be used only once. After that, they appear empty.
    """
    def prime_factors(num: int) -> Iterator[int]:
        """
        Locate prime factors of a number. We handle 2 as a special case to cut the number of
        iterations in half. All prime numbers, except 2, are odd.

        We use one important for loop in addition to recursion. This explicit loop allows us to
        easily handle numbers that have as many as 1,000 factors. Since the for variable, odd_num,
        is not used outside the indented body of the loop, the stateful nature of the odd_num
        variable won't lead to confusion if we make any changes to the body of the loop.

        This example shows how to do tail-call optimization manually. The recursive calls that
        count from 3 to sqrt(num) have been replaced with a loop. The for loop saves us from a
        deeply recursive call stack.

        Because the function is iterable, the 'yield from' statement is used to consume iterable
        values from the recursive call and yield them to the caller.

        Note: In a recursive generator function, be careful of the return statement. Do not use
        'return recursive_iter(args)'. It returns only a generator object; it doesn't evaluate the
        function to return the generated values.
        """
        if num % 2 == 0:
            # If the number is even, we'll yield 2, and then...
            yield 2
            if num // 2 > 1:
                # recursively yield all prime factors of num / 2.
                yield from prime_factors(num // 2)
            return
        for odd_num in range(3, int(math.sqrt(num) + 0.5) + 1, 2):
            # For odd numbers, we'll step through odd values greater than or equal to 3 to locate a
            # candidate factor of the number.
            if num % odd_num == 0:
                # When we locate a factor, odd_num, we'll yield that factor, and then...
                yield odd_num
                if num // odd_num > 1:
                    # recursively yield all prime factors of num / odd_num.
                    yield from prime_factors(num // odd_num)
                return
        # In the event that we can't locate a factor, the number, num, must be prime, so we can
        # yield the number.
        yield num

    assert list(prime_factors(2)) == [2]
    assert list(prime_factors(14)) == [2, 7]
    assert list(prime_factors(18)) == [2, 3, 3]
    assert list(prime_factors(53)) == [53]

# Exploring the limitations of generators


def test_generator_single_use() -> None:
    """Generator functions can be used only once."""
    num_generator = (num for num in range(10))
    assert min(num_generator) == 0
    with pytest.raises(ValueError, match=r"max\(\) arg is an empty sequence"):
        max(num_generator)


def test_generator_multi_use() -> None:
    """Use the itertools.tee() method to overcome the once-only limitation to create clones of the
    generator expression."""
    def limits(iterable: Iterable[int]) -> Tuple[int, int]:
        max_iter, min_iter = itertools.tee(iterable, 2)
        return min(max_iter), max(min_iter)

    num_generator = (num for num in range(10))
    assert limits(num_generator) == (0, 9)

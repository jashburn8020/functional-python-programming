#!/usr/bin/env pytest-3
"""
Introducing Essential Functional Concepts

We'll look at each of the following functional programming topics:
- First-class and higher-order functions, which are sometimes known as pure functions.
- Immutable data.
- Strict and non-strict evaluation. We can also call this eager versus lazy evaluation.
- Recursion instead of an explicit loop state.
- Functional type systems
"""

# pylint:disable=missing-docstring

# Pure functions


def test_pure_function():
    """
    Pure function:
    - conceptually simpler and much easier to test
    - local-only code; avoid global statements, look closely at any use of nonlocal
    - its return value is the same for the same arguments (no variation with local static
    variables, non-local variables, mutable reference arguments or input streams from I/O devices)
    - its evaluation has no side effects (no mutation of local static variables, non-local
    variables, mutable reference arguments or I/O streams).
    - allows some optimizations by changing evaluation order
    - conceptually simpler and much easier to test

    A Python lambda is a pure function - can't have assignment statements
    """
    def mersenne(integer):
        return 2**integer - 1

    assert mersenne(17) == 131071

# Higher-order functions


def test_higher_order_function():
    """
    Higher-order function:
    Functions that accept a function as an argument or return a function as a value. We can use
    higher-order functions as a way to create composite functions from simpler functions.

    Example higher-order function: max(iterable[, default=obj, key=func])
    """

    year_cheese = [(2006, 32.73), (2007, 33.5), (2008, 32.84), (2009, 33.02), (2010, 32.92)]

    # default: return tuple with largest value on position 0
    assert max(year_cheese) == (2010, 32.92)
    # return tuple with largest value in position 1
    assert max(year_cheese, key=lambda yc: yc[1]) == (2007, 33.5)

# Immutable data


def test_wrap_process_unwrap():
    """
    Immutable data:
    Since we're not using variables to track the state of a computation, our focus needs to stay
    on immutable objects. We can make extensive use of tuples and namedtuples to provide more
    complex data structures that are immutable.

    A list of tuples is a fairly common data structure. We will often process this list of tuples
    in one of the two following ways:
    1. Using higher-order functions, e.g., provide lambda as an argument to the max() function
    2. Using the wrap-process-unwrap pattern: In a functional context, we should call this and the
    unwrap(process(wrap(structure))) pattern
    """

    year_cheese = [(2006, 32.73), (2007, 33.5), (2008, 32.84)]

    # wrap: map(lambda yc: (yc[1], yc), year_cheese) - transform each item into a two-tuple with a
    # key followed by the original item; comparison key is yc[1]
    # (map object converted into a list for readability)
    assert list(map(lambda yc: (yc[1], yc), year_cheese)) == [
        (32.73, (2006, 32.73)), (33.5, (2007, 33.5)), (32.84, (2008, 32.84))]

    # process: max() - position zero used for comparison
    assert max(map(lambda yc: (yc[1], yc), year_cheese)) == (33.5, (2007, 33.5))

    # unwrap: subscript [1] - second element of the two-tuple selected by max()
    assert max(map(lambda yc: (yc[1], yc), year_cheese))[1] == (2007, 33.5)

# Strict and non-strict evaluation


def test_non_strict():
    """
    Functional programming's efficiency stems, in part, from being able to defer a computation
    until it's required. Logical expression operators and, or, and if-then-else are all lazy/non
    strict. We sometimes call them short-circuit operators because they don't need to evaluate all
    arguments to determine the resulting value.

    Generator expressions and generator functions are lazy. They don't create all possible results
    immediately.

    (If the body of a def contains yield, the function automatically becomes a generator function.
    yield statement suspends function's execution and sends a value back to the caller, but retains
    enough state to enable the function to resume where it left off.)
    """
    def numbers():
        for i in range(1024):
            yield i

    def sum_to(num: int) -> int:
        total: int = 0
        for i in numbers():
            if i == num:
                break  # does not evaluate the entire result of numbers()
            total += i
        return total

    assert sum_to(5) == 10

# Recursion instead of an explicit loop state


def test_linear_search_imperative():
    def linear_search_imperative(alist, element):
        for elem in alist:
            if elem == element:
                return True
        return False

    assert not linear_search_imperative([1, 2, 3, 5, 8], 4)
    assert linear_search_imperative([1, 2, 3, 5, 8], 5)


def test_linear_search_recursive():
    """
    Functional programs don't rely on loops and the associated overhead of tracking the state of
    loops. Instead, functional programs try to rely on recursive functions.

    While recursion is often succinct and expressive, we have to be cautious about using it in
    Python. There are two problems that can arise:
    1. Python imposes a recursion limit (default is 1000) to detect recursive functions with
    improperly defined base cases
    2. Python does not have a compiler that does TCO (Tail-Call Optimization (TCO) in the compiler
    changes them to loops)

    We'll often optimize a purely recursive function to use an explicit for loop in a generator
    expression.
    """
    def linear_search_recursive(alist, element):
        if not alist:
            return False
        if alist[0] == element:
            return True
        return linear_search_recursive(alist[1:], element)

    assert not linear_search_recursive([1, 2, 3, 5, 8], 4)
    assert linear_search_recursive([1, 2, 3, 5, 8], 5)

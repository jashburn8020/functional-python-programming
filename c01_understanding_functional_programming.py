#!/usr/bin/env pytest-3
"""
Understanding Functional Programming

Functional programming defines a computation using expressions and evaluation; often these are
encapsulated in function definitions. It de-emphasizes or avoids the complexity of state change
and mutable objects.

In an imperative language, such as Python, the state of the computation is reflected by the values
of the variables in the various namespaces; some kinds of statements make a well-defined change to
the state by adding or changing (or even removing) a variable. A language is imperative because
each statement is a command, which changes the state in some way.

In a functional language, we replace the state—the changing values of variables—with a simpler
notion of evaluating functions. Each function evaluation creates a new object or objects from
existing objects. Since a functional program is a composition of functions, we can design lower-
level functions that are easy to understand, and then design higher-level compositions that can
also be easier to visualize than a complex sequence of statements.
"""

# pylint:disable=missing-docstring


# Using the functional paradigm


def test_sum_range_imperative():
    """
    Sum a range of numbers - imperative and procedural. It relies on variables to explicitly show
    the state of the program. They rely on the assignment statements to change the values of the
    variables and advance the computation toward completion.
    """
    total = 0
    for num in range(1, 10):
        if num % 3 == 0 or num % 5 == 0:
            total += num

    assert total == 23


def sum_recursive(seq):
    """
    The sum of a sequence has a simple, recursive definition. We've defined the sum of a sequence
    in two cases:
    - the base case states that the sum of a zero length sequence is 0
    - the recursive case states that the sum of a sequence is the first value plus the sum of the
    rest of the sequence.
    Since the recursive definition depends on a shorter sequence, we can be sure that it will
    (eventually) devolve to the base case.
    """
    if not seq:  # Empty seq is false
        return 0
    return seq[0] + sum_recursive(seq[1:])


def test_sum_recursive():
    assert sum_recursive([1, 2, 3, 4]) == 10


def until(upper_bound, filter_func, value):
    """
    Similarly, a sequence of values can have a simple, recursive definition. We compare a given
    value against the upper bound. If the value reaches the upper bound, the resulting list must be
    empty. This is the base case for the given recursion.

    There are two more cases defined by the given filter_func() function:
    - If the value is passed by the filter_func() function, we'll create a very small list,
    containing one element, and append the remaining values of the until() function to this list.
    - If the value is rejected by the filter_func() function, this value is ignored and the result
    is simply defined by the remaining values of the until() function.

    We can see that the value will increase from an initial value until it reaches the upper bound,
    assuring us that we'll reach the base case soon.
    """
    if value == upper_bound:
        return []
    if filter_func(value):
        return [value] + until(upper_bound, filter_func, value + 1)
    return until(upper_bound, filter_func, value + 1)


def test_sequence_recursive():
    assert until(5, lambda val: isinstance(val, int), 1) == [1, 2, 3, 4]
    assert until(10, lambda val: val % 3 == 0 or val % 5 == 0, 0) == [0, 3, 5, 6, 9]


def test_sum_sequence_functional():
    """
    In a functional sense, the sum of the multiples of three and five can be defined in two parts:
    1. A sequence of values that pass a simple test condition - multiples of three and five
    2. The sum of a sequence of numbers

    sum_recursive() and until() are defined as simple recursive functions. The values are computed
    without resorting to using intermediate variables to store the state.

    Note: Many functional programming language compilers can optimize these kinds of simple
    recursive functions. Python can't do the same optimizations.
    """
    assert sum_recursive(until(10, lambda val: val % 3 == 0 or val % 5 == 0, 0)) == 23


# Using a functional hybrid


def test_functional_hybrid_sum_range():
    """
    Use nested generator expressions to iterate through a collection of values and compute the sum
    of these values. The variable val is bound to each value, more as a way of expressing the
    contents of the set than as an indicator of the state of the computation. It doesn't exist
    outside the binding in the generator expression; it doesn't define the state of the computation.

    List comprehension: conditional construction of list literals using for and if clauses:
    [n for n in range(1, 10) if n % 3 == 0 or n % 5 == 0]

    Generator expression: A high performance, memory efficient generalization of list
    comprehensions and generators. Iterates over the elements one at a time without needing to have
    a full list created in memory.

    Sum using list comprehension - build a full list of squares in memory, iterate over those
    values, and, when the reference is no longer needed, delete the list:
    sum([x*x for x in range(10)])

    Sum using generator expression:
    sum(x*x for x in range(10))
    """
    # sum() consumes the generator expression, creating a final object, 23
    assert sum(val for val in range(1, 10) if val % 3 == 0 or val % 5 == 0) == 23

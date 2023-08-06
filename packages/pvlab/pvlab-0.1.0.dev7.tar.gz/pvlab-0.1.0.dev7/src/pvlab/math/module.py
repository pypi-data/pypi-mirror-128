#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculates the module of a vector (n-components).

It supports n-dimensional components, to apply e.g. in the calculation
of type b uncertainty of calibration, for compatibility with python versions
previous than 3.8, whose function hypot does not support n-dimensional points.
In python v3.8, it was added support for n-dimensional points.
In python 3.10, accuracy was improved.

`Here`_ for further information.

.. _Here: https://docs.python.org/3/library/math.html#trigonometric-functions
"""
from math import sqrt
from typing import Sequence


def module(*components: Sequence[float]) -> float:
    """Calculate the module of a vector, given its components.

    **Example 1**: correct functioning.

    >>> components = [5, 8, 3, 6]

    >>> round(module(*components), 3)
    11.576

    **Example 2**: components must be floats or ints.

    >>> components = [5, 8, 3, '6']

    >>> module(*components)  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: Components items must be 'int' or 'float' type.
    """
    # Check if components members are 'int' or 'float' types.
    for item in components:
        if type(item) not in [int, float]:
            raise TypeError("Components items must be 'int' or 'float' type.")

    module = sqrt(sum(x**2 for x in components))
    return module


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

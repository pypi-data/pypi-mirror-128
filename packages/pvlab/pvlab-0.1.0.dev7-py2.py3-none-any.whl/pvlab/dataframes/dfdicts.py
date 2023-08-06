#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Perform type-conversion and *pretty-print* operations for dictionaries.

It contains the following functions:
"""

import pandas


def dict_to_df(dictionary: dict,
               columns: list) -> pandas.core.frame.DataFrame:
    """Re-arrange a dictionary to become a pandas dataframe.

    It performs a type conversion of a dictionary (e.g. a dictionary that
    represents some kind of valid time intervals),
    returning a ``pandas`` DataFrame.

    **Example 1**: correct functioning.

    >>> dates = {'START_1': (2021,5,5,8,1,0), 'END_1': (2021,5,6,22,52,0)}

    >>> columns = ['%Y', '%m', '%d', '%H', '%M', '%S']

    >>> dict_to_df(dates, columns)
               %Y  %m  %d  %H  %M  %S
    START_1  2021   5   5   8   1   0
    END_1    2021   5   6  22  52   0


    **Example 2**: the columns list is too short.

    >>> columns = ['%Y', '%m', '%d', '%H', '%M']

    >>> dict_to_df(dates, columns)  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Length of columns list is equal to 5, but has to be equal to 6.


    **Example 3**: the columns list is too long.

    >>> columns = ['%Y', '%m', '%d', '%H', '%M', '%S', '%mS']

    >>> dict_to_df(dates, columns)  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Length of columns list is equal to 7, but has to be equal to 6.
    """
    # Determination of maxlength
    maxlength = 0
    if len(dictionary.values()) > 0:
        for item in dictionary.values():
            length = len(item)
            if maxlength <= length:
                maxlength = length
    # Length of columns list must fit with maxlength
    if len(columns) != maxlength:
        raise ValueError(f'Length of columns list is equal to \
{len(columns)}, but has to be equal to \
{maxlength}.')
    df = pandas.DataFrame(data=dictionary.values(),
                          index=dictionary.keys(),
                          columns=columns)
    return df


def print_dict(dictionary: dict,
               columns: list,
               title: str = '') -> None:
    """Prettyprint a dictionary of dates, adding a title.

    **Example**: correct functioning.

    >>> dates = {'START_1': (2021,5,5,8,1,0), 'END_1': (2021,5,6,22,52,0)}

    >>> columns = ['%Y', '%m', '%d', '%H', '%M', '%S']

    >>> title = 'Valid time intervals'

    >>> print_dict(dates, columns, title)
    Valid time intervals
     --------------------
                %Y  %m  %d  %H  %M  %S
    START_1  2021   5   5   8   1   0
    END_1    2021   5   6  22  52   0

    """
    if title:
        subscript = '-' * len(title)
    elif not title:
        subscript = ''
    print(title)
    print(subscript)
    print(dict_to_df(dictionary, columns))


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: BSD 3-clause
# Copyright 2019-2021, José P. Silva. All rights reserved.
# See archive 'LICENSE' for further information.
"""Provide tools to facilitate the selection of relevant data."""

from typing import Iterable


def set_channels(numbers: Iterable[int],
                 names: Iterable[str],
                 nameafter: bool = True) -> Iterable[str]:
    """
    Generate a list of channel names from a set of numbers and a set of names.

    It is designed to automate the selection of specific active
    channels,*e.g.* within data frames containing a big number of data
    columns.
    Given a list of *n* numbers (``numbers``) and *m* names (``names``), it
    generates a list of channel names in the form:

    [
    [**number_1**][**name_1**],
    [**number_1**][**name_2**], ...,
    [**number_1**][**name_m**],
    , ...,
    , ...,
    , ...,
    [**number_n**][**name_1**],
    **number_n**][**name_2**], ...,
    [**number_n**][**name_m**],
    ]

    If argument ``nameafter`` is True (by default), names
    are added after numbers. Otherwise, names are added before numbers.

    Item types (both numbers and names) must be convertible into strings.

    If the ``numbers`` list is empty, it directly retuns the ``names`` list.
    In the same way, if the ``names`` list is empty, it returns the
    ``numbers`` list. Anyway, it performs a previous conversion into ``str``
    types.

    At least one list must not be empty.

    **Example 1**: function ``set_channels``.

    >>> numbers = [101, 115, 207]

    >>> names = ['(Time stamp)', '(VDC)']

    >>> set_channels(numbers, names).__class__ == list
    True

    >>> len(set_channels(numbers, names)) == 6
    True

    >>> channels = set_channels(numbers, names)

    >>> channels[:2]
    ['101(Time stamp)', '101(VDC)']

    >>> channels[2:4]
    ['115(Time stamp)', '115(VDC)']

    >>> channels[4:]
    ['207(Time stamp)', '207(VDC)']
    """
    try:
        assert numbers.__class__ == list
        assert names.__class__ == list
        assert nameafter.__class__ == bool
    except AssertionError:
        print('mandatory types:\n\tnumbers, names: list.\n\tnameafter: bool.')

    try:
        channels = []
        if numbers:
            for number in numbers:
                if names:
                    for name in names:
                        if nameafter is True:
                            channels.append(str(number) +
                                            str(name))
                        else:
                            channels.append(str(name) +
                                            str(number))
                else:
                    channels = []
                    for number in numbers:
                        channels.append(str(number))
        else:
            if names:
                channels = []
                for name in names:
                    channels.append(str(name))
            else:
                raise ValueError('At least one argument must not be empty.')
    except SyntaxError:
        print("items in 'numbers','names' must be convertible into strings.")
    except NameError:
        print("'names' and 'numbers' in text form must be quoted.")
    return channels


def set_channels_grouped(numbergroups: Iterable[list],
                         namegroups: Iterable[list],
                         nameafter: bool = True,
                         unify: bool = True,
                         init_channels: list = []) -> Iterable[str]:
    """Generate a list of channels from multiple sets of numbers and names.

    It applies recursively the fuction ``set_channels`` to multiple sets
    of numbers and names. Therefore, it allows the generation of multiple
    channel names that contains different names.

    Argument ``nameafter`` possesses the same significance than in
    ``set_channels``, and defaults to ``True``.

    If argument ``unify`` (defaults ``True``) is True, function returns
    a unique list of channels. If it is ``False``, function returns
    separate lists.

    **Example 2**: function ``set_channels_grouped``.

    >>> numbers1 = [101, 102, 104]

    >>> numbers2 = [201, 202, 204]

    >>> names1 = ['(Time stamp)', '(voltage)']

    >>> names2 = ['(Time stamp)', '(temperature)']

    >>> channels = set_channels_grouped([numbers1, numbers2], [names1, names2])

    # let's do some checking:
    >>> channels.__class__ == list  # it returns a list
    True
    >>> channels[:2]  # the first two elements ...
    ['101(Time stamp)', '101(voltage)']
    >>> channels[-2:]  # ... and the last two.
    ['204(Time stamp)', '204(temperature)']

    # On the other hand, being...:
    >>> len_1 = len(numbers1) * len(names1)

    # and...:
    >>> len_2 = len(numbers2) * len(names2)

    >>> len(channels) == len_1 + len_2  # the total number of items
    True

    # Finally, all items must be strings...
    >>> [type(item) for item in channels] == [str] * len(channels)
    True
    """
    try:
        assert numbergroups.__class__ == list
        assert namegroups.__class__ == list
        assert nameafter.__class__ == bool
    except AssertionError:
        print("Types:\n\tnumbergroups, namegroups: list.\n\tnameafter: bool.")

    try:
        assert len(numbergroups) == len(namegroups)
    except AssertionError:
        print("Length of 'numbergroups' and 'namegroups' must be equal.")

    try:
        assert [len(numbergroups), len(namegroups)] != [0, 0]
    except AssertionError:
        print("Arguments cannot be empty lists.")

    try:
        if len(numbergroups) == len(namegroups) == 1:
            return set_channels(numbergroups[0],
                                namegroups[0],
                                nameafter=nameafter)
        else:
            channels = init_channels.copy()
            for nbg, nmg in zip(numbergroups, namegroups):
                channels.append(set_channels(nbg, nmg, nameafter=nameafter))
            if unify is True:
                unified = init_channels.copy()
                for chlist in channels:
                    for item in chlist:
                        unified.append(item)
                channels = unified.copy()
            else:
                pass
        return channels
    except TypeError:
        print('Invalid argument type.')


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=1)


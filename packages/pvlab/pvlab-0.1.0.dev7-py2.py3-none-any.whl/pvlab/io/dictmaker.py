# -*- coding: utf-8 -*-
# License: BSD 3-clause

"""Generate python dictionaries from multiple files and data types.

New functions are intended to read files of parameters and convert each
data file into a python dictionary. Different type of parameters should be
located in different files, for a better performance.
"""

import io
from typing import TypeVar, Iterable
import warnings


def get_dict(file: TypeVar('File', str, io.StringIO),
             dtype: str,
             sep: str = ':',
             isStringIO: bool = False) -> dict:
    r"""Generate a python dictionary from a file of parameters.

    Function ``get_dict`` reads a file that contains parameters in the form
    *[name]: [value]* (or in other general form *[name][sep] [value]* if
    specified.
    It requires the type of data to be introduced, admitting
    types ``int``, ``float``, ``tuple`` or ``str`` (unknown data types are
    admitted, but they will be parsed as *raw* strings).
    Originally designed for data-acquisition purposes.
    It also admits ``io.StringIO`` objects instead, if argument ``isStringIO``
    is specified as ``True`` (e.g. for exemplification purposes).

    **Example 1**: ``int`` type arguments:

    >>> data = "readings:21\nminG:600\nrefG:1000"

    >>> settings = get_dict(io.StringIO(data), dtype='int', isStringIO=True)
    >>> settings
    {'readings': 21, 'minG': 600, 'refG': 1000}

    **Example 2**: ``str`` type arguments:

    >>> data = "man.:'manufacturer'\nmod.:'model'\nsn.:'seriesnr'"

    >>> mydict = get_dict(io.StringIO(data), dtype='str', isStringIO=True)
    >>> mydict
    {'man.': 'manufacturer', 'mod.': 'model', 'sn.': 'seriesnr'}
    """
    if dtype not in ['int', 'float', 'tuple', 'dict', 'str']:
        warnings.warn('Unknown type for dtype argument.\n')
        warnings.warn('Arguments will be parsed as raw strings.\n')
    try:
        dictionary = {}
        if not isStringIO:
            with open(file) as file:
                pars_list = file.readlines()
        elif isStringIO:
            pars_list = file.readlines()
        for item in pars_list:
            dict_key = item.split(sep=sep, maxsplit=1)[0]
            dict_val = item.split(sep=sep, maxsplit=1)[1]
            if dtype == 'int':
                dictionary[dict_key] = int(dict_val)
            elif dtype == 'float':
                dictionary[dict_key] = float(dict_val)
            elif dtype == 'tuple':
                dictionary[dict_key] = tuple(dict_val)
            elif dtype == 'str':
                dictionary[dict_key] = eval(str(dict_val))
            else:
                dictionary[dict_key] = str(dict_val)
    except FileNotFoundError as e:
        print(e, '\n File not found. Be sure the file exists.')
    except IndexError as e:
        print(e, '\nAt least one line of file impossible to split.')
    return dictionary


def get_dicts_list(filelist: Iterable[str],
                   dtypelist: Iterable[str],
                   isStringIO: Iterable[bool] = False,
                   sep: str = ':') -> dict:
    r"""Generate a list of dicts from a list of parameter files.

    It uses function ``get_dict`` recursively, from correlative values from /
    ``filelist`` and ``dtypelist`` arguments.

    **Example 1**: source objects containing both ``float`` and ``str`` /
    arguments.

    >>> floatdata = "maxdev:0.02\noffsetthreeshold:2.0"

    >>> filters = io.StringIO(floatdata)  # filename 1 (or StringIO 1)

    >>> strdata = "mode_refpyr:'voltage'\nmode_dut:'currentloop'"

    >>> calmode = io.StringIO(strdata)  # filename 2 (or StringIO 2)

    >>> isstringio = ['True', 'True']

    >>> caliblist = get_dicts_list([filters, calmode], ['float', 'str'], isStringIO=isstringio)

    >>> caliblist[0]
    {'maxdev': 0.02, 'offsetthreeshold': 2.0}

    >>> caliblist[1]
    {'mode_refpyr': 'voltage', 'mode_dut': 'currentloop'}
    """
    dictlist = []
    if type(filelist) != list:
        raise TypeError("filelist argument type must be 'list'.")
    if type(dtypelist) != list:
        raise TypeError("dtypelist argument type must be a 'list'.")
    if type(isStringIO) != list:
        raise TypeError("isStringIO argument type must be a 'list'.")
    if len(filelist) != len(dtypelist):
        raise TypeError('filelist and dtypelist must be of the same length.')
    for filename, dtype, stringio in zip(filelist, dtypelist, isStringIO):
        dictlist.append(get_dict(filename,
                                 dtype,
                                 sep=sep,
                                 isStringIO=stringio))
    return dictlist


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=1)

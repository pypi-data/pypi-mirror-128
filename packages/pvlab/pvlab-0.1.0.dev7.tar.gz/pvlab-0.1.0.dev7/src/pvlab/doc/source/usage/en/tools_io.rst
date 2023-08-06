==============
I/O Management
==============

Provide tools for data input/output.

Create dicts from Source Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:module:: pvlab.io.dictmaker

Generate python dictionaries from multiple files and data types.

New functions are intended to read files of parameters and convert each
data file into a python dictionary. Different type of parameters should be
located in different files, for better performance.

It contains the following functions:

Function get_dict
"""""""""""""""""

.. py:function:: pvlab.io.dictmaker.get_dict(file: TypeVar('File', str, io.StringIO), dtype: str, sep: str = ':', isStringIO: bool = False) -> dict:

   Generate a python dictionary from a file of parameters.

   Function ``get_dict`` reads a file that contains parameters in the form
   *[name]: [value]* (or in other general form *[name][sep] [value]*, if
   specified).
   It requires specifying the type of data contained in the file, admitting
   types ``int``, ``float``, ``tuple`` or ``str`` (unknown data types are
   admitted, but they will be parsed as *raw* strings).
   Originally designed for data-acquisition purposes. It also admits
   ``io.StringIO`` objects instead, if argument ``isStringIO`` is specified
   as ``True`` (e.g. useful for exemplification purposes).

**Example 1**: ``int`` type arguments:

.. code-block:: python

   from io import StringIO
   from pvlab.io.dictmaker import get_dict
   
   data = "readings:21\nminG:600\nrefG:1000"
   settings = get_dict(io.StringIO(data), dtype='int', isStringIO=True)
   # ... argument "io.StringIO(data)" can be replaced by a file name.
   
   settings
   {'readings': 21, 'minG': 600, 'refG': 1000}


**Example 2**: ``str`` type arguments:

.. code-block:: python

   from io import StringIO
   from pvlab.io.dictmaker import get_dict
   
   data = "man.:'manufacturer'\nmod.:'model'\nsn.:'seriesnr'"
   mydict = get_dict(io.StringIO(data), dtype='str', isStringIO=True)
   
   mydict
   {'man.': 'manufacturer', 'mod.': 'model', 'sn.': 'seriesnr'}


Function get_dicts_list
"""""""""""""""""""""""

.. py:function:: pvlab.io.dictmaker.get_dicts_list(filelist: Iterable[str],  dtypelist: Iterable[str], isStringIO: Iterable[bool] = False, sep: str = ':') -> dict:

   Generate a list of dicts from a list of parameter files or ``io.StringIO``
   objects.

   It calls the previous function ``get_dict`` recursively, from correlative
   values of ``filelist`` and ``dtypelist`` arguments.


**Example 3**: source objects containing both ``float`` and ``str`` arguments.

.. code-block:: python

   from io import StringIO
   from pvlab.io.dictmaker import get_dicts_list
   
   floatdata = "maxdev:0.02\noffsetthreeshold:2.0"
   filters = io.StringIO(floatdata)  # StringIO_1 (or filename_1)
   
   strdata = "mode_refpyr:'voltage'\nmode_dut:'currentloop'"
   calmode = io.StringIO(strdata)  # StringIO_2 (or filename_2)
   
   isstringio = ['True', 'True']  # io.StringIO objects? (defaults False)
   caliblist = get_dicts_list([filters, calmode], ['float', 'str'], isStringIO=isstringio)  # it returns a list of python dicts.
   
   caliblist[0]  # ...data from StringIO_1 (or filename_1)
   {'maxdev': 0.02, 'offsetthreeshold': 2.0}
   
   caliblist[1]  # ... data from StringIO_2 (or filename_2)
   {'mode_refpyr': 'voltage', 'mode_dut': 'currentloop'}
   

Create a list of channels
^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:module:: pvlab.io.channels

Provide tools to facilitate the selection of relevant data.

It contains the following functions:

Function set_channels
"""""""""""""""""""""

.. py:function:: pvlab.io.channels.set_channels(numbers: Iterable[int], names: Iterable[int], nameafter: bool = True) -> Iterable[str]:

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

.. code-block:: python

   from pvlab.io.channels import set_channels
   
   numbers = [101, 115, 207]
   names = ['(Time stamp)', '(VDC)']
   
   set_channels(numbers, names).__class__ == list
   True
   len(set_channels(numbers, names)) == 6
   True
   
   channels = set_channels(numbers, names)
   
   channels[:2]
   ['101(Time stamp)', '101(VDC)']
   channels[2:4]
   ['115(Time stamp)', '115(VDC)']
   channels[4:]
   ['207(Time stamp)', '207(VDC)']
   
  
Function set_channels_grouped
"""""""""""""""""""""""""""""
   
.. py:function:: pvlab.io.channels.set_channels_grouped(numbergroups: Iterable[list], namegroups: Iterable[list], nameafter: bool = True, unify: bool = True, init_channels: list = []) -> Iterable[str]:

   Generate a list of channels from multiple lists of numbers and names.
   
   It applies recursively the fuction ``set_channels`` to multiple sets
   of numbers and names. Therefore, it allows the generation of multiple
   channel names that contains different names.
   
   Argument ``nameafter`` possesses the same significance than in
   ``set_channels``, and defaults to ``True``.
    
   If argument ``unify`` (defaults ``True``) is True, function returns 
   a unique list of channels. If it is ``False``, function returns
   separate lists.
   
   If arguments 'numbergroups' and 'namegroups' are not of the same length,
   the shorter one marks the end of parsing, and further terms in the
   larger argument are neglected, so ``numbers3`` argument in an entry like:
   ``set_channels_grouped([numbers1, numbers2, numbers3],
   [names1, names2])`` is neglected, and so it is ``names3`` argument
   in entry ``set_channels_grouped([numbers1, numbers2],
   [names1, names2, names3])``.
   
**Example 2**: function ``set_channels_grouped``.

.. code-block:: python

    from pvlab.io.channels import set_channels_grouped
    
    numbers1 = [101, 102, 104]
    numbers2 = [201, 202, 204]
    
    names1 = ['(Time stamp)', '(voltage)']
    names2 = ['(Time stamp)', '(temperature)']
    
    channels = set_channels_grouped([numbers1, numbers2], [names1, names2])
    
    # let's do some checking:
    channels.__class__ == list  # it should return a list
    True
    channels[:2]  # the first two elements ...
    ['101(Time stamp)', '101(voltage)']
    channels[-2:]  # ... and the last two.
    ['204(Time stamp)', '204(temperature)']
    
    # On the other hand, being ...
    len_1 = len(numbers1) * len(names1)
    # and ...
    len_1 = len(numbers1) * len(names1)
    # the total amount of items generated should be ...
    len(channels) == len_1 + len_2
    True
    
    # Finally, all items must be strings...
    [type(item) for item in channels] == [str] * len(channels)
    True

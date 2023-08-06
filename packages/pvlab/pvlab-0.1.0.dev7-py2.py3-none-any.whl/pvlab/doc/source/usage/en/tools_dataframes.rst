=================
Create Dataframes
=================

.. py:module:: pvlab.dataframes

Provide tools to manage dataframes in the context of calibration.

It contains the following python modules:

DataFrames from dicts
^^^^^^^^^^^^^^^^^^^^^

.. py:module:: pvlab.dataframes.dfdicts

Perform type-conversion and *pretty-print* operations for dictionaries.

It contains the following functions:

Function dict_to_df
"""""""""""""""""""

.. py:function:: dict_to_df(dictionary: dict, columns: list) -> pandas.core.frame.DataFrame

   Re-arrange a dictionary to become a pandas dataframe.
   It performs a type conversion of a dictionary (e.g. a dictionary that
   represents some kind of valid time intervals), returning a pandas.DataFrame.

Code examples:
   
When correct parameters are provided, it **returns** a ``pandas.DataFrame``
object:

**Example 1**: correct use of function ``pvlab.dataframes.dfdicts``.

.. code-block:: python

   >>> from pvlab.dataframes.dfdicts import dict_to_df

   >>> dates = {'START_1': (2021,5,5,8,1,0), 'END_1': (2021,5,6,22,52,0)}

   >>> columns = ['%Y', '%m', '%d', '%H', '%M', '%S']

   >>> dict_to_df(dates, columns)
              %Y  %m  %d  %H  %M  %S
   START_1  2021   5   5   8   1   0
   END_1    2021   5   6  22  52   0

Otherwise, a ``ValueError`` is raised when the length of ``columns``
does not match the length of the values of the given dictionary:

**Example 2**: list of columns shorter than expected.

.. code-block:: python

   >>> from pvlab.dataframes.dfdicts import dict_to_df

   >>> columns = ['%Y', '%m', '%d', '%H', '%M']

   >>> dict_to_df(dates, columns) # doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
       ...
   ValueError: Length of columns list is equal to 5, but has to be equal to 6.

Function print_dict
"""""""""""""""""""

**Example 3**: list of columns longer than expected.

.. code-block:: python

   >>> from pvlab.dataframes.dfdicts import dict_to_df

   >>> columns = ['%Y', '%m', '%d', '%H', '%M', '%S', '%mS']

   >>> dict_to_df(dates, columns) # doctest: +IGNORE_EXCEPTION_DETAIL
   Traceback (most recent call last):
       ...
   ValueError: Length of columns list is equal to 7, but has to be equal to 6.


.. py:function:: print_dict(dictionary: dict, columns: list, title: str = '') -> None

   Prettyprint a dictionary of dates, adding a title.
   It appears to be similar to dict_to_df, but print_dict just print,
   (it does not return a pandas.DataFrame object, it returns None):

**Example 4**: correct use of function ``pvlab.dataframes.print_dict``.

.. code-block:: python

   >>> from pvlab.dataframes.dfdicts import print_dict

   >>> dates = {'START_1': (2021,5,5,8,1,0), 'END_1': (2021,5,6,22,52,0)}

   >>> columns = ['%Y', '%m', '%d', '%H', '%M', '%S']

   >>> title = 'Valid time intervals'

   >>> print_dict(dates, columns, title)
   Valid time intervals
   --------------------
              %Y  %m  %d  %H  %M  %S
   START_1  2021   5   5   8   1   0
   END_1    2021   5   6  22  52   0

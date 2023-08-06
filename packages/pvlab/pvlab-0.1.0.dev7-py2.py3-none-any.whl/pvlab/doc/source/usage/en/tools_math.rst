===============
Math operations
===============

.. py:module:: pvlab.math

Provide tools for mathematical or statistical operations.


Composition
^^^^^^^^^^^

.. py:module:: pvlab.math.module

Composition of quantities, intended for statistical purposes.


Function module
"""""""""""""""

.. py:function:: pvlab.math.module.module(*components: Sequence[float]) -> float:

   Calculate the module of a vector, or the result of a quadratic composition,
   given its components. It supports n-dimensional components.
   It is useful when working with versions of python older than 3.8
   (e.g. for determining the total *type B* uncertainty from homogeneous
   contributions).


.. note::
   In python v3.8, it was added support for n-dimensional points in
   built-in function ``math.hypot``. Then, in python 3.10,
   accuracy was improved. `Here`_ for further information.


**Example 1**: correct use of function ``pvlab.math.module``.

.. code-block:: python

   from pvlab.math.module import module
   
   components = [5, 8, 3, 6]
   
   round(module(*components), 3)
   11.576


**Example 2**: ``components`` must be ``float`` or ``int`` types.

.. code-block:: python

   from pvlab.math.module import module

   components = [5, 3, 8, '6']
   module(*components)
   
   Traceback (most recent call last):
       ...
   TypeError: components items must be int or float types.



.. _Here: https://docs.python.org/3/library/math.html#trigonometric-functions

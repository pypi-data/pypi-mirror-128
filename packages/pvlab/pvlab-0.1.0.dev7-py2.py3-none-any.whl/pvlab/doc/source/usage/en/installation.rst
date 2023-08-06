============
Installation
============

From Python installer
---------------------

From pip, proceed as follows:

First of all, if a virtual environment (e.g. *myvenv*) has been 
previously created, and it is the desired working environment, 
it should be activated. You can do it by typing from 
**Terminal** (in |MacOS (C)|/Unix):

:literal:`source myenv/bin/activate`

or, from a **system console** in |Windows| platforms:

:literal:`.\\myvenv\\Scripts\\activate`

Also, the python installer ``pip`` itself should be updated:

:literal:`python -m pip install --upgrade pip`

.. note::
   Be sure the python root folder is present in the system path.

Finally, the |app| package can be installed:

:literal:`python -m pip install --upgrade pvlab`

From Anaconda IDE
-----------------

When using the `Anaconda IDE`_, |app| can be installed both by typing:

:literal:`conda install pvlab`

or, alternatively, from the |Anaconda| navigator, following the sequence:
*Environments* > *Search Packages*, and selecting the |app| package.

.. _Anaconda IDE: https://www.anaconda.com
.. |MacOS (C)| unicode:: MacOS 0xA9
.. |Windows| unicode:: Windows U+2122
.. |Anaconda| unicode:: Anaconda U+2122

=================
The PVLab Project
=================

Introduction
------------
PVLAB is a project devoted to the development and improvement of scientific
software for the measurement, calibration and modeling of the performance of
photovoltaic devices and solar sensors. PVLAB package born from the efforts
in data treatment performed during the calibration of pyranometers at
the `Laboratory of Photovoltaic Solar Energy (PVLab)`_ of the `Research Center
for Energy, Environment and Technology (CIEMAT)`_ in Madrid, Spain.
In next releases, ``pvlab`` will provide sets of tools, mainly consisting in
classes and functions, to perform the data treatment for the calibration of
pyranometers and other type of solar sensors and photovoltaic devices.
Eventually, ``pvlab`` will try to widen its scope to further calibration
procedures of solar sensors and photovoltaic devices.

History
-------
The origin of ``pvlab`` is a python tool, named ``calibration``, which is
being developed since 2019 in PVLab-CIEMAT for its own use. It was
originally designed to manage the big amount of data generated during
the outdoor measurements, while performing the routine calibration
of pyranometers. 

Soon, both the *Python programming language* and the ``calibration`` tool
themselves proved to be quick and reliable methods for data treatment.
Gradually, the code grew in complexity, whereas new functionalities were
being enabled. Indeed, to the basic requirements of data *I/O* and a first
block of core calculations, some others joined, like fine data-filtering,
determination of error sources and total uncertainty, tools for generation
of reports, graphics and further calibration records.

Finally, when it was concluded the development of the version 2.0.0 of the
application ``calibration``, it became clear that a formal package should
be released, separately from the former tool. By doing so, some of the
resources created are now at disposal of the scientific community, under a
3-clause BSD License.

Development
-----------
One procedure chosen for the early development of ``pvlab`` is that,
as functions and classes created for its use at the lab are being adapted
from their specific purpose to address more general cases, and their
robustness and performance is considered sufficiently tested, they will be
progresively incorporated to the ``pvlab`` library.

In order to clarify the features and abilities of the objects created,
docstrings of relevant functions or classess contain examples, which have
been verified with the python built-in package ``doctest``.
In addition, there is a *test_[module]* ready for each one, checked by using
the *unittest* built-in package.

On the other hand, author's hope is that ``pvlab`` will eventually
turn into a **community-developed library**, so contributions and 
constructive comments are welcome. At this respect, ``pvlab`` adopts the
aim of providing resources in the context of measurement, calibration,
determination of uncertainty, validation techniques and potentially,
many other utilities for the improvement of data treatment for solar sensors
and photovoltaic devices.

In the long term, a more general purpose lies in the background, which
is the advance of data science and the development of software projects for
scientific purposes, even "knocking at the doors" of data mining, machine
learning and deep learning techniques.


.. _Research Center for Energy, Environment and Technology (CIEMAT): https://www.ciemat.es
.. _Laboratory of Photovoltaic Solar Energy (PVLab): pvlab.ciemat.es

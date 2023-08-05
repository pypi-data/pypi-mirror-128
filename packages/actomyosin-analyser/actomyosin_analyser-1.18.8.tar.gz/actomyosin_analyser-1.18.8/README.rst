
``actomyosin_analyser``
***********************

This python package is a collection of analysis tools for polymer data. It was developed
with a focus on output data of actin simulation frameworks
(especially `bead-state-model <https://gitlab.com/ilyas.k/bead_state_model>`_ and
`cytosim <https://gitlab.com/f-nedelec/cytosim>`_, in early versions
also `AFINES <https://github.com/Simfreed/AFINES>`_).

Install
=======

``actomyosin_analyser`` can be installed via pip:

.. code:: bash

   pip install actomyosin-analyser

Docker
------

``actomyosin_analyser`` is also installed in the ``bead_state_model``
`docker image <https://hub.docker.com/r/ilyask/bead_state_model>`_. Details how to install and use it
can be found in the `README <https://gitlab.com/ilyas.k/bead_state_model>`_
and `documentation <http://akbg.uni-goettingen.de/docs/bead_state_model/>`_ of ``bead_state_model``.

Documentation
=============

The documentation can be built (requires ``sphinx`` and the ``sphinx-rtd-theme``) from the source files
provided in the ``docs`` folder (e.g. with command ``make html``). A built version
of the docs can be found `here <http://akbg.uni-goettingen.de/docs/actomyosin_analyser/>`_.

Key Concepts
============

Individual Simulations
----------------------

``actomyosin_analyser`` provides the ``Analyser`` class
(``actomyosin_analyser.analysis.analyser.Analyser``). Methods of
this class allow the user easy access to simulation data and results of analyses
performed with that data. Most data and results can be accessed via methods starting with
``get_``. Most ``get_`` methods use a get/read/compute pattern: when
the ``get_`` method is called for the first time, the results need to be
computed and saved. When it is called the next time, the saved data will be read,
potentially saving a lot of computation time, but increasing the occupied disk space.

The ``Analyser`` works independently of the raw data format. The goal is a unified
analysis interface, no matter how the raw data was created. This is achieved by
externalizing the raw data reading to implementations of the ``DataReader`` class.
In the ``actomyosin_analyser`` package, ``DataReader`` is a abstract base class.
This base class needs to be implemented to match the respective raw data. Implementations
of ``DataReader`` exist for ``bead_state_model`` (in the ``bead_state_model`` package) and
for ``cytosim`` (in the ``cytosim_reader`` `package <https://gitlab.gwdg.de/ikuhlem/cytosim_reader>`_).
Technically, these implementations do not inherit from the base class ``DataReader``, as I did not
want to make ``actomyosin_analyser`` a dependency for either one.

Sets of Simulations
---------------------

``actomyosin_analyser`` offers some means to deal with sets of simulations, where one or multiple
parameters were varied across simulations. Namely, these means
are the ``ExperimentIterator`` class and analysis pipelines. The ``ExperimentIterator`` is
generated from a ``pandas`` table with information on parameter values for each simulation.
Simulations are then grouped by matching parameters. Pipelines make use of these groups,
and can  largely automated compute results of ensembles of simulations. More details can be found
in the documentation.

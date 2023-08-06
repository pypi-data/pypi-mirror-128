.. _installation:

Installation
============

In this section we will explain how to install the Qblox instrument package.
To do this make sure you have `Python 3.8 <https://www.python.org/downloads/release/python-380/>`_ or newer installed.

.. tip::
    The Python version can be queried by running ``$ python --version`` in your terminal of choice.

The Qblox instrument package can be installed through `PIP <https://pip.pypa.io/en/stable/>`_, by executing the following command:

.. code-block:: console

    $ pip install qblox-instruments

This will install the most recent version of the package. Please make sure that the version you install is compatible with your current module firmware
(See `Qblox instruments PyPI <https://pypi.org/project/qblox-instruments/>`_ and section :ref:`getting_started/updating:Updating`). To install a specific version
of the package, execute the following command:

.. code-block:: console

    $ pip install qblox-instruments==<version>

.. tip::
    You can query your installed version by executing ``$ pip show qblox-instruments``.

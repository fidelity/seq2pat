.. _installation:

Installation
============

.. admonition:: Installation Options

	The package can be installed with two options:

	1. Install from PyPI using ``pip install seq2pat``
	2. Build from the source code (more on this in the following sections)

.. _requirements:

Requirements
------------

* The library requires **Python 3.8+**, the ``Cython`` package,  and a ``C++`` compiler (gcc, clang or another). See `requirements.txt`_  for dependencies.

* Make sure that the C++ compiler used in your Python installation is the same or compatible with the C++ compiler that you use to build the Cython artifacts. You can see the underlying C++ compiler of your Python installation using ``python -i``.

* On Windows, you can install `MS Visual Studio Build Tools`_ for the ``C++`` compiler.

* On Mac, you can install `Command Line Tools`_ for the ``Clang`` compiler.

Build from the source code
-----------------------

You can install the library on your platform from a wheel package created by the source code.

.. code-block:: python

	cd seq2pat
	pip install setuptools wheel # if wheel is not installed
	python setup.py build_ext --inplace # make the cython extension also complied for use in the current directory
	python setup.py bdist_wheel
	pip install dist/seq2pat-X.X.X-py3-none-any.whl

.. important:: Don't forget to replace ``X.X.X`` with the current version number.

Test Your Setup
---------------

Successful compilation creates ``Cython`` artifacts in the directory ``build``.

To confirm that the installation was successful, run the tests included in the project.

If you install from PyPI, please also run ``python setup.py build_ext --inplace`` (or ``pip install -e .``) under seq2pat folder to make sure the cython extension also complied for use in the current directory.

All tests should pass.

.. code-block:: python

	cd seq2pat
	python -m unittest discover tests

You can now also import Seq2Pat in a Python shell or notebook.

.. code-block:: python

	from sequential.seq2pat import Seq2Pat, Attribute

For examples of how to use the library, refer to :ref:`Usage Examples<examples>`.

Upgrading the Library
---------------------

To upgrade to the latest version of the library, run ``pip install seq2pat`` or ``git pull origin master`` in the repo folder,
and then run ``pip install --upgrade --no-cache-dir dist/seq2pat-X.X.X-py3-none-any.whl``.

.. _MS Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
.. _Command Line Tools: https://developer.apple.com/
.. _requirements.txt: https://github.com/fidelity/seq2pat/blob/master/requirements.txt

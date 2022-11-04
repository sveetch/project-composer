.. _Python: https://www.python.org/
.. _click: https://palletsprojects.com/p/click/
.. _colorlog: https://github.com/borntyping/python-colorlog
.. _tomli: https://github.com/hukkin/tomli

.. project-composer documentation master file, created by David Thenon

================
Project composer
================

This is a Python composer for modular projects.

Basically, you give it a project manifest that will be uses to organize your various
project parts. Parts can be classes, text files or you can implement another part
kind.


Dependancies
************

* `Python`_>=3.8;
* `click`_ >=8.0;
* `colorlog`_;
* `tomli`_;


Links
*****

* Read the documentation on `Read the docs <https://project-composer.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/project-composer>`_;
* Clone it on its `Github repository <https://github.com/sveetch/project-composer>`_;


User’s Guide
************

.. toctree::
   :maxdepth: 2

   overview.rst
   install.rst
   sample_basic.rst
   cli.rst
   core/index.rst


Developer’s Guide
*****************

.. toctree::
   :maxdepth: 1

   development.rst
   history.rst

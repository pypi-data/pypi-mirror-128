========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-publishextrator/badge/?style=flat
    :target: https://python-publishextrator.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/JonasBrother97/python-publishextrator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/JonasBrother97/python-publishextrator

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/JonasBrother97/python-publishextrator?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/JonasBrother97/python-publishextrator

.. |requires| image:: https://requires.io/github/JonasBrother97/python-publishextrator/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/JonasBrother97/python-publishextrator/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/JonasBrother97/python-publishextrator/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/JonasBrother97/python-publishextrator

.. |version| image:: https://img.shields.io/pypi/v/publishextrator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/publishextrator

.. |wheel| image:: https://img.shields.io/pypi/wheel/publishextrator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/publishextrator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/publishextrator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/publishextrator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/publishextrator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/publishextrator

.. |commits-since| image:: https://img.shields.io/github/commits-since/JonasBrother97/python-publishextrator/v0.0.3.svg
    :alt: Commits since latest release
    :target: https://github.com/JonasBrother97/python-publishextrator/compare/v0.0.0...master



.. end-badges

PublishNews extractor

* Free software: BSD 2-Clause License

Installation
============

::

    pip install publishextrator

You can also install the in-development version with::

    pip install https://github.com/JonasBrother97/python-publishextrator/archive/master.zip


Documentation
=============


https://python-publishextrator.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

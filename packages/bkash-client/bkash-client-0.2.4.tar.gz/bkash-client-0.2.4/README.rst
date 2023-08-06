========
Overview
========

A Client for BKash API.

**Free software: Mozilla Public License Version 2.0**

Disclaimer
===========

Work in progress! DO NOT USE!


Why?
====

A client library should be intuitive to use, rich in coding aid (e.g. typing and validation). We hope to meet that standard.

Features
=========
* Pydantic powered dataclasses for every request (in request one can also use :code:`dict` that will be converted to a `dataclass`) and response.
* Methods for all official endpoints.

Installation
============

::

    pip install bkash-client

You can also install the in-development version with::

    pip install https://gitlab.com/codesigntheory/python-bkash-client/-/archive/master/python-bkash-client-master.zip


Documentation
=============


https://python-bkash-client.readthedocs.io/


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

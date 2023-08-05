.. image:: https://img.shields.io/pypi/v/setuptools_hacks.bypass_summary_newline.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/setuptools_hacks.bypass_summary_newline.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/setuptools_hacks.bypass_summary_newline

.. image:: https://github.com/jaraco/setuptools_hacks.bypass_summary_newline/workflows/tests/badge.svg
   :target: https://github.com/jaraco/setuptools_hacks.bypass_summary_newline/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2021-informational
   :target: https://blog.jaraco.com/skeleton


Setuptools plugin that works around the failure when a package's Summary (aka description) may contain a newline. Install this alongside setuptools to bypass the error for this invalid input in legacy environments.

======================
charmonium.determ_hash
======================

.. image: https://img.shields.io/pypi/dm/charmonium.determ_hash
   :alt: PyPI Downloads
.. image: https://img.shields.io/pypi/l/charmonium.determ_hash
   :alt: PyPI Downloads
.. image: https://img.shields.io/pypi/pyversions/charmonium.determ_hash
   :alt: Python versions
.. image: https://img.shields.io/github/stars/charmoniumQ/charmonium.determ_hash?style=social
   :alt: GitHub stars
.. image: https://img.shields.io/librariesio/sourcerank/pypi/charmonium.determ_hash
   :alt: libraries.io sourcerank

- `PyPI`_
- `GitHub`_

.. _`PyPI`: https://pypi.org/project/charmonium.determ_hash/
.. _`GitHub`: https://github.com/charmoniumQ/charmonium.determ_hash

This library provides a deterministic hash for Python objects. |hash|_ will give
different results each process invocation, in order to thwart denial-of-service
attacks based on intentionally triggering hash collisions (see ``-R`` in
`Python's CLI options`_). Even setting ``PYTHONHASHSEED`` is not enough, because
the hash can still use non-deterministic data such as pointer-addresses. By
default, this package uses the `xxhash`_ algorithm, which is the fastest
non-cryptographic hash I know of.

>>> from charmonium.determ_hash import determ_hash
>>> determ_hash(b"hello world")
141361478936837800319111455324245712876

.. |hash| replace:: ``hash``
.. _`hash`: https://docs.python.org/3/library/functions.html?highlight=hash#hash
.. _`Python's CLI options`: https://docs.python.org/3/using/cmdline.html
.. _`xxhash`: https://cyan4973.github.io/xxHash/

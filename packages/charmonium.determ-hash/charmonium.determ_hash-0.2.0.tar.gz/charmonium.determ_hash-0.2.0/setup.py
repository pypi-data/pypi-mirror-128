# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['charmonium', 'charmonium.determ_hash']

package_data = \
{'': ['*']}

install_requires = \
['xxhash>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'charmonium.determ-hash',
    'version': '0.2.0',
    'description': '',
    'long_description': '======================\ncharmonium.determ_hash\n======================\n\n.. image: https://img.shields.io/pypi/dm/charmonium.determ_hash\n   :alt: PyPI Downloads\n.. image: https://img.shields.io/pypi/l/charmonium.determ_hash\n   :alt: PyPI Downloads\n.. image: https://img.shields.io/pypi/pyversions/charmonium.determ_hash\n   :alt: Python versions\n.. image: https://img.shields.io/github/stars/charmoniumQ/charmonium.determ_hash?style=social\n   :alt: GitHub stars\n.. image: https://img.shields.io/librariesio/sourcerank/pypi/charmonium.determ_hash\n   :alt: libraries.io sourcerank\n\n- `PyPI`_\n- `GitHub`_\n\n.. _`PyPI`: https://pypi.org/project/charmonium.determ_hash/\n.. _`GitHub`: https://github.com/charmoniumQ/charmonium.determ_hash\n\nThis library provides a deterministic hash for Python objects. |hash|_ will give\ndifferent results each process invocation, in order to thwart denial-of-service\nattacks based on intentionally triggering hash collisions (see ``-R`` in\n`Python\'s CLI options`_). Even setting ``PYTHONHASHSEED`` is not enough, because\nthe hash can still use non-deterministic data such as pointer-addresses. By\ndefault, this package uses the `xxhash`_ algorithm, which is the fastest\nnon-cryptographic hash I know of.\n\n>>> from charmonium.determ_hash import determ_hash\n>>> determ_hash(b"hello world")\n141361478936837800319111455324245712876\n\n.. |hash| replace:: ``hash``\n.. _`hash`: https://docs.python.org/3/library/functions.html?highlight=hash#hash\n.. _`Python\'s CLI options`: https://docs.python.org/3/using/cmdline.html\n.. _`xxhash`: https://cyan4973.github.io/xxHash/\n',
    'author': 'Samuel Grayson',
    'author_email': 'grayson5@illinois.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/charmoniumQ/charmonium.determ_hash.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

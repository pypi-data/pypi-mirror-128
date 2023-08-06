# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pydupes']
install_requires = \
['click>=7,<8', 'tqdm>=4,<5']

entry_points = \
{'console_scripts': ['pydupes = pydupes:main']}

setup_kwargs = {
    'name': 'pydupes',
    'version': '0.0.0',
    'description': 'Yet another duplicate file finder that may be faster in environments with millions of files and terabytes of data or over high latency filesystems.',
    'long_description': None,
    'author': 'Erik Reed',
    'author_email': 'erik.reed@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

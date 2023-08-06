# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pydupes']
install_requires = \
['click', 'tqdm>=4,<5']

entry_points = \
{'console_scripts': ['pydupes = pydupes:main']}

setup_kwargs = {
    'name': 'pydupes',
    'version': '0.0.1',
    'description': 'A duplicate file finder that may be faster in environments with millions of files and terabytes of data.',
    'long_description': '`pydupes` is yet another duplicate file finder like rdfind/fdupes et al\nthat may be faster in environments with millions of files and terabytes\nof data or over high latency filesystems (e.g. NFS).\n\nThe algorithm is similar to [rdfind](https://github.com/pauldreik/rdfind) with threading and consolidation of\nfiltering logic (instead of separate passes).\n- traverse the input paths, collecting the inodes and file sizes\n- for each set of files with the same size:\n  - further split by matching 4KB on beginning/ends of files\n  - for each non-unique (by size, boundaries) candidate set, compute the sha256 and emit pairs with matching hash\n\nConstraints:\n- traversals do not span multiple devices\n- symlink following not implemented\n- concurrent modification of a traversed directory could produce false duplicate pairs \n(modification after hash computation)\n\n### Install\n```bash\npip3 install --user --upgrade pydupes\n```\n\n### Usage\n\n```bash\n# Collect counts and stage the duplicate files, null-delimited source-target pairs:\npydupes /path1 /path2 --progress --output dupes.txt\n\n# Sanity check a hardlinking of all matches:\nxargs -0 -n2 echo ln --force --verbose {} {} < dupes.txt\n```\n\n### Benchmarks\n\n',
    'author': 'Erik Reed',
    'author_email': 'erik.reed@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/erikreed/pydupes',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prototype_python_library']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'prototype-python-library',
    'version': '0.1.1',
    'description': 'A prototype python library.',
    'long_description': None,
    'author': 'Nuno Costa',
    'author_email': '91nunocosta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

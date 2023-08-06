# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydme']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydme',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

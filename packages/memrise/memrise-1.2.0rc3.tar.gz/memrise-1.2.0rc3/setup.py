# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memrise', 'memrise.data', 'memrise.extract', 'memrise.googletrans']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'memrise',
    'version': '1.2.0rc3',
    'description': 'Scraping the vocabulary from the Memrise course',
    'long_description': None,
    'author': 'Joseph Quang',
    'author_email': 'tquangsdh20@hcmut.edu.vn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

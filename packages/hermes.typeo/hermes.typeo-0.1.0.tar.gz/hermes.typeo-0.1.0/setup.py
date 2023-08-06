# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hermes', 'hermes.typeo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hermes.typeo',
    'version': '0.1.0',
    'description': 'Utilities for running functions as scripts',
    'long_description': 'None',
    'author': 'Alec Gunny',
    'author_email': 'alec.gunny@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

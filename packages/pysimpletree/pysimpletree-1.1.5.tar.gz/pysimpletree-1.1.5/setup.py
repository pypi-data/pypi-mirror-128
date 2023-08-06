# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysimpletree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysimpletree',
    'version': '1.1.5',
    'description': 'https://github.com/joaocarlos-losfe/pysimpletree',
    'long_description': None,
    'author': 'João Carlos && Vitor Santos',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

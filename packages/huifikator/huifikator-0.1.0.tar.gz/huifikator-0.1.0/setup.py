# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['huifikator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'huifikator',
    'version': '0.1.0',
    'description': 'Lexical reduplication library',
    'long_description': None,
    'author': 'CatCoderr',
    'author_email': 'catcoderr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fabdb_sdk',
 'fabdb_sdk.enums',
 'fabdb_sdk.exceptions',
 'fabdb_sdk.helpers',
 'fabdb_sdk.models',
 'fabdb_sdk.repositories']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'fabdb-sdk',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rubem Mota',
    'author_email': 'rubemmota89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carnival_contrib', 'carnival_contrib.caddy']

package_data = \
{'': ['*']}

install_requires = \
['carnival>=3.0.0']

setup_kwargs = {
    'name': 'carnival-contrib',
    'version': '3.0.0',
    'description': 'Carnival community receipts',
    'long_description': None,
    'author': 'Dmirty Simonov',
    'author_email': 'demalf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

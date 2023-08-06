# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocurrencylayer']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<1']

setup_kwargs = {
    'name': 'aiocurrencylayer',
    'version': '1.0.2',
    'description': 'Python client for interacting with the CurrencyLayer API',
    'long_description': None,
    'author': 'Fabian Affolter',
    'author_email': 'fabian@affolter-engineering.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/home-assistant-ecosystem/aiocurrencylayer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geld', 'geld.asyncio', 'geld.common', 'geld.sync']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'geld',
    'version': '0.2.1',
    'description': 'A library to handle money operations',
    'long_description': '# Geld\n\nA library to easily handle currency conversions\n',
    'author': 'Affonso Brian Pereira Azevedo',
    'author_email': 'contato.affonsobrian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/affonsobrian/geld',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

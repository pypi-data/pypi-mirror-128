# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fxlang', 'fxlang.core']

package_data = \
{'': ['*']}

install_requires = \
['lark>=0.11.3,<0.12.0',
 'printree>=0.2.0,<0.3.0',
 'typing-extensions>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'fxlang',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Bernardo Lourenço',
    'author_email': 'bernardo.martins.lourenco@everis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eth_sdk',
 'eth_sdk.abi_management',
 'eth_sdk.config',
 'eth_sdk.sdk',
 'eth_sdk.system']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click==7.1.1',
 'dotsi>=0.0.3,<0.0.4',
 'requests>=2.26.0,<3.0.0',
 'web3>=5.24.0,<6.0.0']

entry_points = \
{'console_scripts': ['eth-sdk = eth_sdk.shell:cli']}

setup_kwargs = {
    'name': 'eth-sdk',
    'version': '0.0.1',
    'description': 'SDK to interact with EVM compatible blockchains',
    'long_description': None,
    'author': 'Arugulo',
    'author_email': 'arugulo@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)

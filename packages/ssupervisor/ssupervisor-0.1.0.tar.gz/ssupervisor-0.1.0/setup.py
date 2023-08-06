# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssupervisor', 'ssupervisor.lib']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'rich>=10.14.0,<11.0.0', 'watchdog>=2.1.6,<3.0.0']

setup_kwargs = {
    'name': 'ssupervisor',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Infinium',
    'author_email': 'infinium-llc@protonamil.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

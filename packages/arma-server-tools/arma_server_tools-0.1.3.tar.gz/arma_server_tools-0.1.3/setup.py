# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arma_server_tools']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click-log==0.3.1',
 'click>=8.0.3,<9.0.0',
 'colorama==0.4.3',
 'pyyaml>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['arma_server = arma_server_tools.arma_server:main',
                     'steam_pull = arma_server_tools.workshop:main']}

setup_kwargs = {
    'name': 'arma-server-tools',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Ryan',
    'author_email': 'citizen.townshend@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

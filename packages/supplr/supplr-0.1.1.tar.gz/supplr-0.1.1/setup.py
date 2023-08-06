# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supplr']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1', 'pandas>=1.3.4']

entry_points = \
{'console_scripts': ['supplr = supplr.main:cli']}

setup_kwargs = {
    'name': 'supplr',
    'version': '0.1.1',
    'description': 'supplr CLI application for management Marathon board',
    'long_description': None,
    'author': 'GreenLab',
    'author_email': 'greenlab@jinr.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

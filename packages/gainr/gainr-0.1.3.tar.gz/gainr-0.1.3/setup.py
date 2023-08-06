# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gainr']

package_data = \
{'': ['*']}

install_requires = \
['Flask-RESTful>=0.3.9,<0.4.0',
 'Flask>=2.0.2,<3.0.0',
 'PyYAML>=5.3.1',
 'click>=8.0.3,<9.0.0',
 'gpiozero>=1.6.2,<2.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['gainr = gainr.main:cli']}

setup_kwargs = {
    'name': 'gainr',
    'version': '0.1.3',
    'description': 'Gainr is a HTTP API and CLI application for managing VGA amplifiers',
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

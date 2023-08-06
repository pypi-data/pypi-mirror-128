# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrostarter', 'pyrostarter.commands']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0']

entry_points = \
{'console_scripts': ['pyrostarter = pyrostarter.pyrostarter:main']}

setup_kwargs = {
    'name': 'pyrostarter',
    'version': '0.2.1',
    'description': 'Pyrogram CLI Template Creator',
    'long_description': None,
    'author': 'ahmetveburak',
    'author_email': 'ahmetbozyurtt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

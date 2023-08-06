# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oppapi']

package_data = \
{'': ['*']}

install_requires = \
['okome>=0.0.1,<0.0.2', 'pyserde>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'oppapi',
    'version': '0.0.1',
    'description': '',
    'long_description': '# `oppapī`\n\n*Option parser on top of dataclasses, inspired by structopt.*\n\n<p align="center">\n  <img src="logo.png" width=25% />\n</p>\n\n## Overview\n\n',
    'author': 'yukinarit',
    'author_email': 'yukinarit84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yukinarit/oppapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybookmd', 'pybookmd.generators']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'fastcore==1.3.19',
 'packaging==20.9',
 'pypandoc==1.5',
 'pyparsing==2.4.7']

entry_points = \
{'console_scripts': ['build = pybookmd.cli:build_book']}

setup_kwargs = {
    'name': 'pybookmd',
    'version': '1.0.7',
    'description': '"Simple book building CLI for markdown based books"',
    'long_description': None,
    'author': 'Dylan Kirby',
    'author_email': 'dylankirbydev@outlook.com',
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

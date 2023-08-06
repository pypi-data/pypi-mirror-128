# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secretm']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pycryptodome>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'secretm',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'baileywickham',
    'author_email': 'baileywickham@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

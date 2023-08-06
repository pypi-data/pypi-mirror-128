# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytrombone']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'pytrombone',
    'version': '0.1.0',
    'description': 'Wrapper for the Trombone project',
    'long_description': None,
    'author': 'Gabriel Couture',
    'author_email': 'gacou54@ulaval.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

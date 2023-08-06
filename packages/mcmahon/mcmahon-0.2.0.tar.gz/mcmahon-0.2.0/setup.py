# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcmahon']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'mcmahon',
    'version': '0.2.0',
    'description': 'McMahon Tournament Manager',
    'long_description': None,
    'author': 'Oleksandr Hiliazov',
    'author_email': 'oleksandr.hiliazov@eleks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)

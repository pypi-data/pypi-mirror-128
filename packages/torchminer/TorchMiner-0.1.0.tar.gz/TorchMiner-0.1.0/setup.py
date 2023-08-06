# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchminer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'torchminer',
    'version': '0.1.0',
    'description': 'A Package To ',
    'long_description': None,
    'author': 'InEase',
    'author_email': 'inease28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

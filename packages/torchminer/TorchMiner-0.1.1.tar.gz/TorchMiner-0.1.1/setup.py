# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchminer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'torchminer',
    'version': '0.1.1',
    'description': 'Run Torch With A Simple Miner',
    'long_description': 'This Project is Forked From [MineTorch](https://github.com/louis-she/minetorch).\n\n',
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

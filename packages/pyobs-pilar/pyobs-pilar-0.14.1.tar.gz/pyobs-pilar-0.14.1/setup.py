# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyobs_pilar']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyobs-pilar',
    'version': '0.14.1',
    'description': 'pyobs model for Pilar TCS',
    'long_description': None,
    'author': 'Tim-Oliver Husser',
    'author_email': 'thusser@uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)

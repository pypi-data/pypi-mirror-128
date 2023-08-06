# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyobs_asi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyobs-asi',
    'version': '0.14.0',
    'description': 'pyobs model for ASI cameras',
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

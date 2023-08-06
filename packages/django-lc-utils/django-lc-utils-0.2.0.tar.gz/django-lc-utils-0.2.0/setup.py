# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_lc_utils', 'django_lc_utils.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.13,<4.0.0', 'django-model-utils>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'django-lc-utils',
    'version': '0.2.0',
    'description': 'Utilities for Django application',
    'long_description': None,
    'author': 'Tejas Bhandari',
    'author_email': 'tejas@thesummitgrp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

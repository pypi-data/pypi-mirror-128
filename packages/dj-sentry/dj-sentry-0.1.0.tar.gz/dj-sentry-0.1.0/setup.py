# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_sentry']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0,<4.0', 'sentry-sdk>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'dj-sentry',
    'version': '0.1.0',
    'description': 'A Django app to initialize Sentry client for your Django applications',
    'long_description': None,
    'author': 'Michael Vieira',
    'author_email': 'dev@mvieira.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

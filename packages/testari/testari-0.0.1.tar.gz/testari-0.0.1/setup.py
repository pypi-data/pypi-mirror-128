# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testari']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'testari',
    'version': '0.0.1',
    'description': 'End to end test runner',
    'long_description': 'End to end test runner.\n',
    'author': 'Thomas Cellerier',
    'author_email': 'thomas.cellerier@appgate.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/appgate/testari',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)

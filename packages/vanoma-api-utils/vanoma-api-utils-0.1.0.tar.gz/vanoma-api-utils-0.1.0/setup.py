# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vanoma_api_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vanoma-api-utils',
    'version': '0.1.0',
    'description': 'Python utils for vanoma APIs',
    'long_description': None,
    'author': 'Vanoma',
    'author_email': 'contact@vanoma.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

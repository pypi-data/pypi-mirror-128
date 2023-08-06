# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vanoma_api_utils',
 'vanoma_api_utils.django',
 'vanoma_api_utils.rest_framework']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.9,<4.0.0',
 'djangorestframework-camel-case>=1.2.0,<2.0.0',
 'djangorestframework>=3.12.4,<4.0.0']

setup_kwargs = {
    'name': 'vanoma-api-utils',
    'version': '0.4.0',
    'description': 'Python utils for vanoma APIs',
    'long_description': None,
    'author': 'Vanoma',
    'author_email': 'contact@vanoma.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

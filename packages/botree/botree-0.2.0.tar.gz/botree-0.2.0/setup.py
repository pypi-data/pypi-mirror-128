# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botree']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.19.8,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'botree',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'ericmiguel',
    'author_email': 'ericmiguel@id.uff.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

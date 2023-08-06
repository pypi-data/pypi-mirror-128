# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timeless']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.2,<2.0.0',
 'dateutils>=0.6.12,<0.7.0',
 'pydantic>=1.8.2,<2.0.0',
 'pymongo>=3.12.0,<4.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'timeless',
    'version': '0.1.0',
    'description': 'Human friendly datetime utilities.',
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

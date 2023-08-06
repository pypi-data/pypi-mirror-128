# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['microdata_validator']

package_data = \
{'': ['*'],
 'microdata_validator': ['metadata_ref/Attribute/*',
                         'metadata_ref/Identifier/*',
                         'metadata_ref/SubjectField/*',
                         'metadata_ref/UnitType/*',
                         'metadata_ref/ValueDomain/*']}

install_requires = \
['jsonschema>=4.2.1,<5.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-dotenv>=0.5.2,<0.6.0',
 'pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'microdata-validator',
    'version': '0.0.2',
    'description': 'Python package for validating datasets in the microdata platform',
    'long_description': None,
    'author': 'microdata-developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

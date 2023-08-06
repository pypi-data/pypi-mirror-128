# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['validator903', 'validator903.util']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.17.5',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas==1.0.5',
 'quality-lac-data-ref-authorities==2021.4a6',
 'quality-lac-data-ref-postcodes>=2021.8a3,<2022.0']

setup_kwargs = {
    'name': 'quality-lac-data-validator',
    'version': '0.2.0a2',
    'description': 'Shared module for validating the ruleset on the SSDA903 census using DfE rules.',
    'long_description': None,
    'author': 'Mark Waddoups',
    'author_email': 'mark.waddoups@socialfinance.org.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SocialFinanceDigitalLabs/quality-lac-data-beta-validator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

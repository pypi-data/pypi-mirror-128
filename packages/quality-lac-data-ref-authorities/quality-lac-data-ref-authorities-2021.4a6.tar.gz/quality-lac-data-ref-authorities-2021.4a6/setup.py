# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qlacref_authorities']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'quality-lac-data-ref-authorities',
    'version': '2021.4a6',
    'description': 'This is a redistribution of the ONS dataset on Lower Tier Local Authority toUpper Tier Local Authority Lookup packaged for the Quality Lac Data project.Source: Office for National Statistics licensed under the Open Government Licence v.3.0',
    'long_description': None,
    'author': 'Office for National Statistics',
    'author_email': 'sharedcustomercontactcentre@ons.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

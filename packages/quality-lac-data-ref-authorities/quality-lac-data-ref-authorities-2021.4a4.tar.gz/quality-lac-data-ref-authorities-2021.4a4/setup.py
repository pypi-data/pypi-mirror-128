# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qlacref_authorities']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<2.0.0']

extras_require = \
{'feather': ['pyarrow>=6.0.1,<7.0.0']}

setup_kwargs = {
    'name': 'quality-lac-data-ref-authorities',
    'version': '2021.4a4',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

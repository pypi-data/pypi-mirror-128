# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temprc']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.1.11,<2.0.0']

entry_points = \
{'console_scripts': ['temprc = temprc:main']}

setup_kwargs = {
    'name': 'temprc',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Sample README',
    'author': 'subbarayudu',
    'author_email': 'subbarayudu@micropyramid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

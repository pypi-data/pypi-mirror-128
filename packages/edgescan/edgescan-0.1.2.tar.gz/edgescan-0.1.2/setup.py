# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edgescan',
 'edgescan.api',
 'edgescan.cli',
 'edgescan.cli.command_groups',
 'edgescan.data',
 'edgescan.data.types',
 'edgescan.http']

package_data = \
{'': ['*']}

install_requires = \
['hodgepodge>=2.3.3,<3.0.0']

entry_points = \
{'console_scripts': ['edgescan = edgescan.cli:cli']}

setup_kwargs = {
    'name': 'edgescan',
    'version': '0.1.2',
    'description': 'An API client for EdgeScan',
    'long_description': None,
    'author': 'Tyler Fisher',
    'author_email': 'tylerfisher@tylerfisher.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

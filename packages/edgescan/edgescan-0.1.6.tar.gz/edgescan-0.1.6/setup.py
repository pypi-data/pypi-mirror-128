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
    'version': '0.1.6',
    'description': 'An API client for EdgeScan',
    'long_description': "# edgescan  \n\n[![](https://img.shields.io/pypi/pyversions/edgescan)](https://pypi.org/project/edgescan/) [![](https://img.shields.io/pypi/wheel/edgescan)](https://pypi.org/project/edgescan/#files) [![](https://img.shields.io/pypi/l/edgescan)](https://github.com/whitfieldsdad/edgescan/blob/main/LICENSE.md)\n\n---\n\n`edgescan` is a client for [EdgeScan's](https://www.edgescan.com/) [REST API](https://s3-eu-west-1.amazonaws.com/live-cdn-content/docs/api-guide-latest.pdf) that allows you to:\n\n- Query and count assets, hosts, vulnerabilities, and licenses via the command line or programmatically.\n\n## Installation\n\nTo install `edgescan` using `pip`:\n\n```shell\n$ pip install edgescan\n```\n\nTo install `edgescan` from source (requires [`poetry`](https://github.com/python-poetry/poetry)):\n\n```shell\n$ git clone git@github.com:whitfieldsdad/edgescan.git\n$ cd edgescan\n$ make install\n```\n\nTo install `edgescan` from source using `setup.py` (i.e. if you're not using `poetry`):\n\n```shell\n$ git clone git@github.com:whitfieldsdad/edgescan.git\n$ cd edgescan\n$ python3 setup.py install\n```\n\n## Environment variables\n\n|Name              |Default value      |Required|\n|------------------|-------------------|--------|\n|`EDGESCAN_API_KEY`|                   |true    |\n|`EDGESCAN_HOST`   |`live.edgescan.com`|false   |\n\n## Testing\n\nYou can run the integration tests for this package as follows:\n\n```shell\n$ make test\n```\n\n> Note: the integration tests will only be run if the `EDGESCAN_API_KEY` environment variable has been set.\n\n## Tutorials\n\n### Command-line interface\n\nAfter installing `edgescan` you can access the command-line interface as follows:\n\nIf you're using `poetry`:\n\n```shell\n$ poetry run edgescan\nUsage: edgescan [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --host TEXT     ${EDGESCAN_HOST} ✖\n  --api-key TEXT  ${EDGESCAN_API_KEY} ✔\n  --help\n\nCommands:\n  assets           Query or count assets.\n  hosts            Query or count hosts.\n  licenses         Query or count licenses.\n  vulnerabilities  Query or count vulnerabilities.\n```\n\nIf you're not using `poetry`:\n\n```shell\n$ python3 -m edgescan.cli\n```\n\n#### Assets\n\nThe following options are available when working with assets:\n\n```shell\n$ poetry run edgescan assets --help\nUsage: edgescan assets [OPTIONS] COMMAND [ARGS]...\n\n  Query or count assets.\n\nOptions:\n  --help\n\nCommands:\n  count-assets\n  get-asset\n  get-asset-tags\n  get-assets\n```\n\n##### List assets\n\nThe following options are available when listing assets:\n\n```shell\n$ poetry run edgescan assets get-assets --help\nUsage: edgescan assets get-assets [OPTIONS]\n\nOptions:\n  --ids TEXT\n  --names TEXT\n  --tags TEXT\n  --limit INTEGER\n  --help\n```\n\n#### Hosts\n\nThe following options are available when working with hosts:\n\n```shell\n$ poetry run edgescan hosts --help\nUsage: edgescan hosts [OPTIONS] COMMAND [ARGS]...\n\n  Query or count hosts.\n\nOptions:\n  --help\n\nCommands:\n  count-hosts\n  get-host\n  get-hosts\n```\n\n##### List hosts\n\nThe following options are available when listing hosts:\n\n```shell\n$ poetry run edgescan hosts get-hosts --help\nUsage: edgescan hosts get-hosts [OPTIONS]\n\nOptions:\n  --ids TEXT\n  --hostnames TEXT\n  --asset-ids TEXT\n  --asset-tags TEXT\n  --ip-addresses TEXT\n  --os-types TEXT\n  --os-versions TEXT\n  --alive / --dead\n  --limit INTEGER\n  --help\n```\n\n#### Licenses\n\nThe following options are available when working with licenses:\n\n```shell\n$ poetry run edgescan licenses --help\nUsage: edgescan licenses [OPTIONS] COMMAND [ARGS]...\n\n  Query or count licenses.\n\nOptions:\n  --help\n\nCommands:\n  count-licenses\n  get-license\n  get-licenses\n```\n\n##### List licenses\n\nThe following options are available when listing licenses:\n\n```shell\n$ poetry run edgescan licenses get-licenses --help\nUsage: edgescan licenses get-licenses [OPTIONS]\n\nOptions:\n  --ids TEXT\n  --names TEXT\n  --expired / --not-expired\n  --limit INTEGER\n  --help\n```\n\n#### Vulnerabilities\n\nThe following options are available when working with vulnerabilities:\n\n```shell\n$ poetry run edgescan vulnerabilities --help\nUsage: edgescan vulnerabilities [OPTIONS] COMMAND\n                                [ARGS]...\n\n  Query or count vulnerabilities.\n\nOptions:\n  --help\n\nCommands:\n  count-vulnerabilities\n  get-vulnerabilities\n  get-vulnerability\n```\n\n##### List vulnerabilities\n\nThe following options are available when listing vulnerabilities:\n\n```shell\n$ poetry run edgescan vulnerabilities get-vulnerabilities --help\nUsage: edgescan vulnerabilities get-vulnerabilities \n           [OPTIONS]\n\nOptions:\n  --ids TEXT\n  --names TEXT\n  --cve-ids TEXT\n  --asset-ids TEXT\n  --asset-tags TEXT\n  --ip-addresses TEXT\n  --affects-pci-compliance / --does-not-affect-pci-compliance\n  --include-application-layer-vulnerabilities / --exclude-application-layer-vulnerabilities\n  --include-network-layer-vulnerabilities / --exclude-network-layer-vulnerabilities\n  --limit INTEGER\n  --help\n```\n",
    'author': 'Tyler Fisher',
    'author_email': 'tylerfisher@tylerfisher.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whitfieldsdad/edgescan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipfabric']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.1,<0.22.0']

setup_kwargs = {
    'name': 'ipfabric',
    'version': '0.0.1',
    'description': 'Python package for interacting with IP Fabric',
    'long_description': '# IPFabric\n\nIPFabric is a Python module for connecting to and communicating against an IP Fabric instance. \n\n## Installation\n```\npip install ipfabric\n```\n\n## Introduction\n\n## Development\n\nIPFabric uses poetry for the python packaging module.  Install poetry globally:\n```\npip install poetry\n```\n\nTo install a virtual environment run the following command in the root of this directory.\n```\npoetry install\n```\n\nTo build and publish:\n```\npoetry build\npoetry publish\n```\n',
    'author': 'Justin Jeffery',
    'author_email': 'justin.jeffery@ipfabric.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

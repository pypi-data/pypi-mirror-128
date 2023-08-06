# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['maptiler', 'maptiler.cloud_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['maptiler-cloud = maptiler.cloud_cli:cli']}

setup_kwargs = {
    'name': 'maptiler-cloud-cli',
    'version': '1.1.1',
    'description': 'CLI utility for MapTiler Cloud',
    'long_description': '# MapTiler Cloud CLI\n\n## Installation\n\n```shell\npip install maptiler-cloud-cli\n```\n\n## Authorization\n\nYou need an API token to be able to use the tool.\nSpecify it either on the command line or as an environment variable.\nThe token can be acquired from "Credentials" section of your account administration in MapTiler Cloud.\n\n```shell\nmaptiler-cloud --token=MY_TOKEN ...\n```\n\n```shell\nMAPTILER_TOKEN=MY_TOKEN; maptiler-cloud ...\n```\n\n## Usage\n\nTo create a new tileset, use the `tiles ingest` command.\n\n```shell\nmaptiler-cloud tiles ingest v1.mbtiles\n```\n\nThe command will print out the tileset ID on the last line.\nYou can use it to upload a new file to the same tileset.\n\n```shell\nmaptiler-cloud tiles ingest --document-id=EXISTING_TILESET_ID v2.mbtiles\n```\n',
    'author': 'MapTiler',
    'author_email': 'info@maptiler.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maptiler/maptiler-cloud-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

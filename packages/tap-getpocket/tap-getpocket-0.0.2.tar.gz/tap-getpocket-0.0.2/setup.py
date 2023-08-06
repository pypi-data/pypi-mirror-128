# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_getpocket', 'tap_getpocket.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.3.13,<0.4.0']

entry_points = \
{'console_scripts': ['tap-getpocket = tap_getpocket.tap:TapGetPocket.cli']}

setup_kwargs = {
    'name': 'tap-getpocket',
    'version': '0.0.2',
    'description': '`tap-getpocket` is a Singer tap for GetPocket, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Elena Velte',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)

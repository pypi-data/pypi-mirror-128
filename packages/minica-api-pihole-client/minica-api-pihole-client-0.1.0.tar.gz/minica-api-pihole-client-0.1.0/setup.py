# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['minica_api_pihole']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'dataclasses-json>=0.5.6,<0.6.0',
 'paho-mqtt>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['minica-pihole-sync = minica_api_pihole.main:main']}

setup_kwargs = {
    'name': 'minica-api-pihole-client',
    'version': '0.1.0',
    'description': 'Inject minica-api domain messages into pihole dns',
    'long_description': None,
    'author': 'Bjørn Snoen',
    'author_email': 'bjorn.snoen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

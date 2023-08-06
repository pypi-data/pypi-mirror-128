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
{'console_scripts': ['minica-pihole-sync = minica_api_pihole.main:main',
                     'minica-pihole-sync-install = '
                     'minica_api_pihole.main:install',
                     'minica-pihole-sync-uninstall = '
                     'minica_api_pihole.main:uninstall']}

setup_kwargs = {
    'name': 'minica-api-pihole-client',
    'version': '0.3.0',
    'description': 'Inject minica-api domain messages into pihole dns',
    'long_description': '# Minica API pihole client\nA program for listening to domain discoveries published by [minica-api](https://github.com/bjornsnoen/minica-api)\nand injecting them into the custom DNS list used by pihole.\n\n## Installation\n`$ pip install minica-api-pihole-client`\n\nYou will probably want to install this package as root, as the DNS list at `/etc/pihole/custom.list` is owned\nby root. Alternatively chown that file so this program is allowed to overwrite it as the running user.\n\n## Usage\n`$ minica-pihole-sync MQTT-HOST [-p mqttport] [-t domaintopic]`\n',
    'author': 'Bjørn Snoen',
    'author_email': 'bjorn.snoen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bjornsnoen/minica-api-pihole-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

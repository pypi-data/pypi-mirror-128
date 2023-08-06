# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wgconf']

package_data = \
{'': ['*']}

install_requires = \
['Pillow==8.3.1',
 'inquirerpy==0.3.0',
 'pfzy==0.3.3',
 'prompt-toolkit==3.0.22',
 'qrcode==7.2',
 'wcwidth==0.2.5']

entry_points = \
{'console_scripts': ['wgconf = wgconf.prompt:main']}

setup_kwargs = {
    'name': 'wgconf',
    'version': '0.4.0',
    'description': 'Interactive Wireguard configuration generator',
    'long_description': None,
    'author': 'Andy Ta',
    'author_email': 'doktorfaustus@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

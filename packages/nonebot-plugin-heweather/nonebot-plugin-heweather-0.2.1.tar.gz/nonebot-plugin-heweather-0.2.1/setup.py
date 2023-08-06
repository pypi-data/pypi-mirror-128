# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_heweather']

package_data = \
{'': ['*'],
 'nonebot_plugin_heweather': ['resource/backgroud.png',
                              'resource/backgroud.png',
                              'resource/font.ttc',
                              'resource/font.ttc',
                              'resource/icon/*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0', 'httpx>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'nonebot-plugin-heweather',
    'version': '0.2.1',
    'description': 'Get Heweather information and convert to pictures',
    'long_description': None,
    'author': 'kexue',
    'author_email': 'x@kexue.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

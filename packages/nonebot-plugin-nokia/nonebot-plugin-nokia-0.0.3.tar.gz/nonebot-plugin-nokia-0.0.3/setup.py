# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_nokia']

package_data = \
{'': ['*'], 'nonebot_plugin_nokia': ['res/*']}

install_requires = \
['pillow>=8.4.0,<9.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-nokia',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'kexue',
    'author_email': 'xana278@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)

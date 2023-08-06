# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mactidy']

package_data = \
{'': ['*']}

install_requires = \
['Send2Trash>=1.8.0,<2.0.0',
 'configparser>=5.1.0,<6.0.0',
 'pandas>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'mactidy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'NhimHB',
    'author_email': 'chienvq@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

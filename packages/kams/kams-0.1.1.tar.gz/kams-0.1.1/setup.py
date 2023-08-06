# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kams', 'kams.utils']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2.2,<2.0.0', 'click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['kams = kams.__main__:main']}

setup_kwargs = {
    'name': 'kams',
    'version': '0.1.1',
    'description': 'A macro lang for KeeperRL',
    'long_description': None,
    'author': 'GameDungeon',
    'author_email': 'gamedungeon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['locli']

package_data = \
{'': ['*']}

install_requires = \
['hiredis>=2.0.0,<3.0.0', 'loguru>=0.5.3,<0.6.0', 'redis>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['exam1 = examples.exam1:main']}

setup_kwargs = {
    'name': 'locli',
    'version': '0.3.9',
    'description': '',
    'long_description': None,
    'author': 'wonjae.h',
    'author_email': 'warren@telelian.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

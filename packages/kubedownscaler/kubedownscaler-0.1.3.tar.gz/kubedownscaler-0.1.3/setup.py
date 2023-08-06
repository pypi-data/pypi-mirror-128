# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kubedownscaler']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0', 'kubernetes>=19.15.0,<20.0.0']

entry_points = \
{'console_scripts': ['script_name = kubedownscaler:main']}

setup_kwargs = {
    'name': 'kubedownscaler',
    'version': '0.1.3',
    'description': 'Scale down and restore deployments and statefulsets',
    'long_description': None,
    'author': 'Jonathan Gazeley',
    'author_email': 'me@jonathangazeley.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flumes']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.42.0,<4.0.0',
 'SQLAlchemy>=1.4.26,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

entry_points = \
{'console_scripts': ['flumes-discovery = flumes.discoverer:run']}

setup_kwargs = {
    'name': 'flumes',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Jorge Zapata',
    'author_email': 'jorgeluis.zapata@gmail.com',
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

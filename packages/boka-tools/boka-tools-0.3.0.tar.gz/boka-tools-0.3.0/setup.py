# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boka_tools',
 'boka_tools.planning',
 'boka_tools.soil_investigation',
 'boka_tools.soil_investigation.boiler_plates',
 'boka_tools.soil_investigation.json',
 'boka_tools.soil_investigation.sql',
 'boka_tools.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.27', 'pandas>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'boka-tools',
    'version': '0.3.0',
    'description': 'package for general automation work at Boskalis',
    'long_description': None,
    'author': 'Maarten Betman',
    'author_email': 'maarten.betman@boskalis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)

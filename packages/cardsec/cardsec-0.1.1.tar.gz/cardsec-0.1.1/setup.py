# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cardsec']

package_data = \
{'': ['*']}

install_requires = \
['distro>=1.6.0,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'simple-term-menu>=1.4.1,<2.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['cardsec = cardsec.main:main']}

setup_kwargs = {
    'name': 'cardsec',
    'version': '0.1.1',
    'description': 'System and Security Assesment Tool for Cardano SPOs.',
    'long_description': '<h1>Cardsec</h1>\n<h3>Security Assessment Tool for Cardano SPOs</h3>\n<br>\n<p>\n  <h3> Prerequisites </h3>\n  <ul>\n    <li> Linux System\n    <li> Python 3.6 or above\n  </ul>\n</p>\n<br>\n<p>\n  <h3> Installation </h3>\n\n```python\n  sudo pip install cardsec\n```\n</p>\n<br>\n',
    'author': 'Advait Joglekar',
    'author_email': 'advaitjoglekar@yahoo.in',
    'maintainer': 'Advait Joglekar',
    'maintainer_email': 'advaitjoglekar@yahoo.in',
    'url': 'https://github.com/SkryptLabs/Cardsec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

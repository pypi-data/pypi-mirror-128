# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['borg_find']

package_data = \
{'': ['*']}

install_requires = \
['cached-property', 'colorama']

entry_points = \
{'console_scripts': ['borg-find = borg_find.cli:run']}

setup_kwargs = {
    'name': 'borg-find',
    'version': '0.2.0',
    'description': 'Tool to search files in borg archives',
    'long_description': None,
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['changelog_pre_commit']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0']

setup_kwargs = {
    'name': 'changelog-pre-commit',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jorge Alvarado',
    'author_email': 'alvaradosegurajorge@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

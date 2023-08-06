# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proman_versioning', 'proman_versioning.cli', 'proman_versioning.grammars']

package_data = \
{'': ['*'], 'proman_versioning': ['templates/*']}

install_requires = \
['GitPython>=3.1.19,<4.0.0',
 'argufy>=0.1.1-alpha.12,<0.2.0',
 'compendium>=0.1.1-alpha.2,<0.2.0',
 'jinja2>=2.11.2,<3.0.0',
 'lark-parser>=0.10.0,<0.11.0',
 'packaging>=20.9,<21.0',
 'transitions>=0.8.4,<0.9.0']

setup_kwargs = {
    'name': 'proman-versioning',
    'version': '0.1.1a0',
    'description': 'Project Manager Versioning tool.',
    'long_description': None,
    'author': 'Jesse P. Johnson',
    'author_email': 'jpj6652@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['me_backup']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'click>=8.0.1,<9.0.0',
 'python-crontab>=2.5.1,<3.0.0',
 'wakeonlan>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'me-backup',
    'version': '0.1.18',
    'description': 'Simple linux backup controled by a YAML file.',
    'long_description': None,
    'author': 'Lucas',
    'author_email': 'lucasbmello96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

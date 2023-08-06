# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['primapy_plogging']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primapy-plogging',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'team amops',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

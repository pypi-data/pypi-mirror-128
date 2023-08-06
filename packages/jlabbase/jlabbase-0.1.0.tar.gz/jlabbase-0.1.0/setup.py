# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jlabbase']

package_data = \
{'': ['*']}

install_requires = \
['jupyterlab', 'numpy', 'pandas']

setup_kwargs = {
    'name': 'jlabbase',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

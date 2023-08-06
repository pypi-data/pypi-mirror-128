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
    'version': '0.2.0',
    'description': 'This is a small package wit jupyterlab, numpy and pandas. This package serves as base for larger jupyterlab packages.',
    'long_description': None,
    'author': 'yZg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sklearn2json']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.2,<2.0.0', 'scikit-learn>=0.24.2,<0.25.0', 'scipy>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'sklearn2json',
    'version': '2021.5',
    'description': 'Python library for converting Scikit-Learn models to JSON.',
    'long_description': None,
    'author': 'MONTANA Knowledge Management ltd.',
    'author_email': 'info@distiller.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<=3.10',
}


setup(**setup_kwargs)

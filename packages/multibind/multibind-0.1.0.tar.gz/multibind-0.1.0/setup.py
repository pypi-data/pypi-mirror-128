# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multibind']

package_data = \
{'': ['*']}

install_requires = \
['MDAnalysis>=2.0.0,<3.0.0',
 'matplotlib>=3.5.0,<4.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'scipy>=1.7.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'multibind',
    'version': '0.1.0',
    'description': 'A package to find optimal state free energies from a thermodynamic graph.',
    'long_description': None,
    'author': 'Ian Kenney',
    'author_email': 'ikenney@asu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

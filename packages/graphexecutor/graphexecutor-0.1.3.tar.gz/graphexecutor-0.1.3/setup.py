# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graphexecutor', 'graphexecutor.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'dask>=2021.8.1,<2022.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'networkx>=2.6.2,<3.0.0',
 'rich>=10.9.0,<11.0.0']

entry_points = \
{'console_scripts': ['ge = graphexecutor.app:main']}

setup_kwargs = {
    'name': 'graphexecutor',
    'version': '0.1.3',
    'description': 'Graphed based execution of Python paradigms',
    'long_description': None,
    'author': 'siranipour',
    'author_email': 'si292@cam.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

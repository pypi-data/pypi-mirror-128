# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['src', 'src.domain', 'src.services', 'src.use_cases']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'diagrams>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'hexagonal-sanity-check',
    'version': '0.0.13',
    'description': 'Hexagonal Sanity Check',
    'long_description': None,
    'author': 'rfrezino',
    'author_email': 'rodrigofrezino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

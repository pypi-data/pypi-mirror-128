# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captif_slp']

package_data = \
{'': ['*']}

install_requires = \
['captif-data-structures>=0.8,<0.9',
 'click>=8.0.1,<9.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'pandas>=1.3.3,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'captif-slp',
    'version': '0.1',
    'description': '',
    'long_description': '# captif-slp',
    'author': 'John Bull',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/captif-nz/captif-slp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)

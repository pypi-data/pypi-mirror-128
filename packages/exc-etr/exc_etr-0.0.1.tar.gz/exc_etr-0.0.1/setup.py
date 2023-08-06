# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exc_etr']

package_data = \
{'': ['*']}

install_requires = \
['exc-motherclass>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'exc-etr',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

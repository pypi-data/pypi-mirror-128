# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flunt']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.11b1,<22.0', 'isort>=5.10.1,<6.0.0', 'pydocstyle>=6.1.1,<7.0.0']

setup_kwargs = {
    'name': 'flunt',
    'version': '0.2.0',
    'description': 'Python implementation of Domain Notification Pattern based in Flunt (.NET) developed by @andrebaltieri',
    'long_description': None,
    'author': 'Emerson Delatorre',
    'author_email': '38289677+Delatorrea@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

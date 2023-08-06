# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protopypes', 'protopypes.base', 'protopypes.tools']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.5b1,<22.0', 'pretty-errors>=1.2.24,<2.0.0']

setup_kwargs = {
    'name': 'protopypes',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mike-fi',
    'author_email': '77098525+mike-fi@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

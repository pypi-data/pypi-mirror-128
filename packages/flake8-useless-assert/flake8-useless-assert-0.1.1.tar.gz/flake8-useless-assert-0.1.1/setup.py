# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_useless_assert']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.1,<5.0.0']

entry_points = \
{'flake8.extension': ['ULA = flake8_useless_assert:UselessAssert']}

setup_kwargs = {
    'name': 'flake8-useless-assert',
    'version': '0.1.1',
    'description': 'flake8 plugin to catch useless `assert` statements',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

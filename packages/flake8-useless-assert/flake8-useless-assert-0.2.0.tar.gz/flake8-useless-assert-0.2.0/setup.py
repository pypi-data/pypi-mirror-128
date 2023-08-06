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
    'version': '0.2.0',
    'description': 'flake8 plugin to catch useless `assert` statements',
    'long_description': '# flake8-useless-assert\nflake8 plugin to catch useless `assert` statements\n\n\n# Examples of what it will flag\n\n```py\nassert "string literal"\nassert 0x2a\nassert "call to {0}".format("format")\nassert f"f-{str}ing"\nassert True\nassert ...\n```\n\n\n# Testing\nI haven\'t set up proper testing yet, but you can run `poetry install` and then:\n```\nflake8 examples/\n```',
    'author': 'decorator-factory',
    'author_email': 'decorator-factory@yandex.ru',
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

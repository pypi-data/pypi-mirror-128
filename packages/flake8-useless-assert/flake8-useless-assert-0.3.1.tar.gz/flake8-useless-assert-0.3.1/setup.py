# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_useless_assert']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.9,<5.0']

entry_points = \
{'flake8.extension': ['ULA = flake8_useless_assert:UselessAssert']}

setup_kwargs = {
    'name': 'flake8-useless-assert',
    'version': '0.3.1',
    'description': 'flake8 plugin to catch useless `assert` statements',
    'long_description': '# flake8-useless-assert\nflake8 plugin to catch useless `assert` statements\n\n\n# Violations\n\n| Code    | Description                      |   Example                        |\n|---------|----------------------------------|----------------------------------|\n| ULA001  | `assert` with a literal          | `assert "foo"`                   |\n|         |                                  | `assert ...`                     |\n|         |                                  | `True`                           |\n| ULA002  | `assert` with a formatted string | `assert "foo {0}".format(bar)`   |\n|         |                                  | `assert f"foo {bar}"`            |\n\nNote that `assert False` is exempt from `ULA001` because it\'s a common idiom.\n\n# Testing\nI haven\'t set up proper testing yet, but you can run `poetry install` and then:\n```\nflake8 examples/\n```',
    'author': 'decorator-factory',
    'author_email': 'decorator-factory@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decorator-factory/flake8-useless-assert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

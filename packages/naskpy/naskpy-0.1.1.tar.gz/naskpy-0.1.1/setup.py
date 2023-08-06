# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['naskpy']

package_data = \
{'': ['*']}

install_requires = \
['Pillow==8.4', 'pendulum>=2.1.2,<3.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'naskpy',
    'version': '0.1.1',
    'description': 'Tools, modules and functions that I use regularly while coding in Python',
    'long_description': '# NaskPy\n\nTools, modules and functions that I use regularly while coding scripts in Python\n\n[![Maintainability](https://api.codeclimate.com/v1/badges/6f79c1172b6dc903377c/maintainability)](https://codeclimate.com/github/naskio/naskpy/maintainability)\n[![codecov](https://codecov.io/gh/naskio/naskpy/branch/main/graph/badge.svg?token=7HY2KN5428)](https://codecov.io/gh/naskio/naskpy)\n![GitHub branch checks state](https://img.shields.io/github/checks-status/naskio/naskpy/main)\n\n![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/naskio/naskpy)\n![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/naskio/naskpy)\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/naskio/naskpy/Test/main)\n![PyPI](https://img.shields.io/pypi/v/naskpy)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/naskpy)\n\n[![GitHub issues](https://img.shields.io/github/issues/naskio/naskpy)](https://github.com/naskio/naskpy/issues)\n[![GitHub forks](https://img.shields.io/github/forks/naskio/naskpy)](https://github.com/naskio/naskpy/network)\n[![GitHub stars](https://img.shields.io/github/stars/naskio/naskpy)](https://github.com/naskio/naskpy/stargazers)\n![Lines of code](https://img.shields.io/tokei/lines/github/naskio/naskpy)\n[![GitHub license](https://img.shields.io/github/license/naskio/naskpy)](https://github.com/naskio/naskpy/blob/main/LICENSE)\n\n## Test\n\n```shell\npoetry run python -m unittest discover\n```\n',
    'author': 'Mehdi Nassim KHODJA',
    'author_email': 'khodjamehdinassim@gmail.com',
    'maintainer': 'Mehdi Nassim KHODJA',
    'maintainer_email': 'khodjamehdinassim@gmail.com',
    'url': 'https://github.com/naskio/naskpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)

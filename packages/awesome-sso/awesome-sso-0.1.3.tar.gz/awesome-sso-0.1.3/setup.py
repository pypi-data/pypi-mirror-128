# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awesome_sso', 'awesome_sso.exceptions']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.4,<2.0', 'coveralls>=3.3.1,<4.0.0']

setup_kwargs = {
    'name': 'awesome-sso',
    'version': '0.1.3',
    'description': 'sso general utility for services connected to sso',
    'long_description': "[![Stable Version](https://img.shields.io/pypi/v/awesome-sso?label=stable)](https://pypi.org/project/awesome-sso/)\n[![tests](https://github.com/MoBagel/awesome-sso/workflows/ci/badge.svg)](https://github.com/MoBagel/awesome-sso)\n[![Coverage Status](https://coveralls.io/repos/github/MoBagel/awesome-sso/badge.svg?branch=develop)](https://coveralls.io/github/MoBagel/awesome-sso)\n\n# Usage\n## Installing Poetry\n1. create your own environment for poetry, and simply run: `pip install poetry`\n2. alternatively, you can refer to [poetry's official page](https://github.com/python-poetry/poetry)\n\n## Contributing\n1. project setup: `poetry install`\n2. create your own branch to start developing new feature.\n3. before creating pr, make sure you pass `poe lint` and `poe test`.\n4. for a list of available poe command, `poe`\n\n## Publishing\n1. update version in `pyproject.toml`\n",
    'author': 'Schwannden Kuo',
    'author_email': 'schwannden@mobagel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MoBagel/awesome-sso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

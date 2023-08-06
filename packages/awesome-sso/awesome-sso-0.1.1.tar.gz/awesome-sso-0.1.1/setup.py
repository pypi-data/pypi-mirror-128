# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awesome_sso', 'awesome_sso.exceptions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'awesome-sso',
    'version': '0.1.1',
    'description': 'sso general utility for services connected to sso',
    'long_description': '# Usage\n1. to install poetry: `pip instala poetry`\n2. project setup: `poetry install`\n3. update version in `pyproject.toml`\n4. build: `poetry build`\n5. publish to pypi: `poetry publish`\n\n',
    'author': 'Schwannden Kuo',
    'author_email': 'schwannden@mobagel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://gitlab.ct.mobagel.com:7979/MOD/awesome-sso',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

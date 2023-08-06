# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_version']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.4.6,<0.6.0']

setup_kwargs = {
    'name': 'poetry-version',
    'version': '0.2.0',
    'description': 'Python library for extracting version from poetry pyproject.toml file (deprecated)',
    'long_description': '# poetry-version (deprecated)\n\n## What to use instead\n\nNow there is a better way to extract the version of the package.\n\nAssuming your package is named `mypackage`:\n```python\nimport importlib.metadata\n\n__version__ = importlib.metadata.version("mypackage")\n```\n\nThis code should work as is if you are using Python >= 3.8.\n\nFor Python 3.6 and 3.7 you need to install a backport: https://pypi.org/project/importlib-metadata/\n',
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rominf/poetry-version',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)

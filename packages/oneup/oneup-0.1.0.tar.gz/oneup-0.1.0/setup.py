# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oneup']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0',
 'requirements-parser>=0.2.0,<0.3.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['oneup = oneup.cli:main']}

setup_kwargs = {
    'name': 'oneup',
    'version': '0.1.0',
    'description': 'A CLI tool to check for dependency updates for Python, in Python',
    'long_description': "# OneUp\n\nA CLI tool to check for dependency updates for Python, in Python.\n\n## What's this?\n\n`oneup` is a simple command-line interface to aid developers in determining the most recent version of their project's dependencies, as specified in files such as `requirements.txt` and `pyproject.toml`.\n\nRight now, the tool can parse your dependency lists and report the latest version of all your dependencies to the standard output. In the future, the tool might add some other features such as: automatically updating your lists with a latest version, if desired, and only showing the latest version of dependencies if they differ from your currently specified version (or range).\n\n## Installation\n\nYou can use your Python package manager (e.g. [pip](https://pip.pypa.io/en/stable/)) to install `oneup`.\n\n```bash\npip install oneup\n```\n\n## Usage\n\n`oneup` comes with a command-line interface and will automatically detect any supported dependency files in the current directory:\n\n```bash\noneup\n```\n\nYou can also specify which file to check:\n\n```bash\noneup --file path/to/requirements.txt\n```\n\nA complete list of arguments and flags can be found by running:\n\n```bash\noneup --help\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate; a minimum coverage of 75% is expected (and enforced by Github Actions!).\n\n## License\n\nThis project is licensed under the [GNU Affero General Public License v3.0](https://github.com/aitorres/oneup/blob/main/LICENSE).\n",
    'author': 'Andrés Ignacio Torres',
    'author_email': 'dev@aitorres.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aitorres/oneup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

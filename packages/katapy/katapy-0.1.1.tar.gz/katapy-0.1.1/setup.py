# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['katapy']

package_data = \
{'': ['*']}

install_requires = \
['invoke>=1.6.0,<2.0.0', 'pre-commit>=2.15.0,<3.0.0', 'tox>=3.24.4,<4.0.0']

entry_points = \
{'console_scripts': ['kat = katapy.program:program.run',
                     'katapy = katapy.program:program.run']}

setup_kwargs = {
    'name': 'katapy',
    'version': '0.1.1',
    'description': 'A tool for assisting python developers',
    'long_description': '# KataPy\n\nA tool for assisting python developers\n\n[![Built with Cookiecutter Python Package](https://img.shields.io/badge/built%20with-Cookiecutter%20Python%20Package-ff69b4.svg?logo=cookiecutter)](https://github.com/91nunocosta/python-package-cookiecutter)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![Code Coverage](coverage.svg)\n\n## Usage\n\nPrint help:\n\n```bash\nkatapy\n```\n\n## Contributing\n\n### How to prepare the development environment\n\n1. Clone the repository.\n\n   ```bash\n   git clone git@github.com:91nunocosta/katapy.git\n   ```\n\n2. Open the project directory.\n\n   ```bash\n   cd katapy\n   ```\n\n3. Install [_poetry_](https://python-poetry.org/) _package and dependency manager_.\nFollow the [poetry installation guide](https://python-poetry.org/docs/#installation).\nChose the method that is more convenient to you, for example:\n\n   ```bash\n   curl -sSL\\\n        https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \\\n      | python -\n   ```\n\n4. Create a new virtual environment (managed by _poetry_) with the project dependencies.\n\n   ```bash\n   poetry install\n   ```\n\n5. Enter the virtual environment.\n\n   ```bash\n   poetry shell\n   ```\n\n### How to check code quality\n\n1. Prepare the development environment, as described in\n[**How to prepare the development environment**](#how-to-prepare-the-development-environment).\n\n2. Run katapy check command to verify the code quality:\n\n   - all checks:\n\n     ```bash\n     katapy check\n     ```\n\n   - only check source code using [_pre-commit_](https://pre-commit.com/):\n\n     ```bash\n     katapy -s precommit.run\n     ```\n\n   - only test package, using [tox](https://tox.wiki/en/latest/) and [_pytest_](https://docs.pytest.org/en/6.2.x/):\n\n     ```bash\n     katapy -s tox.run\n     ```\n',
    'author': 'Nuno Costa',
    'author_email': '91nunocosta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/91nunocosta/katapy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

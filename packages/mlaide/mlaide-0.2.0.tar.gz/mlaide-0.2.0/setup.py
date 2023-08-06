# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlaide',
 'mlaide._api_client',
 'mlaide._api_client.api',
 'mlaide._api_client.dto',
 'mlaide.model']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0',
 'cloudpickle>=1.6.0,<2.0.0',
 'dataclasses-json>=0.5.2,<0.6.0',
 'httpx>=0.16.1,<0.17.0',
 'marshmallow>=3.10.0,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'mlaide',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Python Client Library for ML Aide\n[![CI pipeline](https://github.com/MLAide/python-client/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/MLAide/python-client/actions/workflows/ci-pipeline.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MLAide_python-client&metric=alert_status)](https://sonarcloud.io/dashboard?id=MLAide_python-client)\n\n## Run example scripts\nIn `examples/` you can find some python scripts as an example.\nThe shell scripts can be used for easier usage.\n\nRun the following commands once in a terminal session\n```shell script\ncs/\nsource ./set_api_key.sh\n```\n\nAfter that you can use the following command to run the scripts\nover and over again:\n```shell script\n./run_example.sh\n```\n\n## Contribution\n### Prerequisites\n1. Install [Python](https://www.python.org/)\n2. Install [Python Poetry](https://python-poetry.org/docs/#installation)\n3. Optional - Install IDE: [PyCharm](https://www.jetbrains.com/pycharm/) \nor [Visual Studio Code](https://code.visualstudio.com/)\n\n### Setup Environment\n1. Install environment and download dependencies\n    ```shell\n   poetry install\n   ```\n   \n2. Activate environment\n    ```shell\n    poetry shell\n    ```\n\n### Run Tests\n```\npytest\n```\n\n### Run Tests with Coverage\n```\ncoverage run --branch --source mlaide -m pytest\ncoverage html\n```\n\n### Build\n```\npoetry build\n```\n\n### Publish (on PyPI)\n```\npoetry publish\n```\n\n## Links\n\n- **Homepage:** https://mlaide.com\n- **Quickstart:** https://docs.mlaide.com/start/quickstart/\n- **Tutorial:** https://docs.mlaide.com/tutorial/introduction/\n- **Documentation:** https://docs.mlaide.com/\n',
    'author': 'Raman Singh',
    'author_email': 'mail.raman.s@gmail.com',
    'maintainer': 'Raman Singh',
    'maintainer_email': 'mail.raman.s@gmail.com',
    'url': 'https://mlaide-ai.web.app/home',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

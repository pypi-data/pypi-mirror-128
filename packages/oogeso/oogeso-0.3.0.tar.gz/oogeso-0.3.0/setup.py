# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oogeso',
 'oogeso.core',
 'oogeso.core.devices',
 'oogeso.core.networks',
 'oogeso.dto',
 'oogeso.io',
 'oogeso.plots',
 'oogeso.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Pyomo>=6.1.2,<7.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pyarrow>=6.0.1,<7.0.0',
 'pydot>=1.4.2,<2.0.0',
 'scipy>=1.7.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'oogeso',
    'version': '0.3.0',
    'description': 'Offshore Oil and Gas Field Energy System Operational Optimisation (OOGESO)',
    'long_description': '<p>\n<a href="https://badge.fury.io/gh/oogeso%2Foogeso"><img src="https://badge.fury.io/gh/oogeso%2Foogeso.svg" alt="GitHub version" height="18"></a>\n<a href="https://github.com/oogeso/oogeso/actions/workflows/build.yml?query=workflow%3ACI"><img src="https://img.shields.io/github/workflow/status/oogeso/oogeso/CI"></a>\n<a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9-blue.svg"></a>\n<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://lgtm.com/projects/g/oogeso/oogeso/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/oogeso/oogeso.svg?logo=lgtm&logoWidth=18"/></a>\n<a href="https://lgtm.com/projects/g/oogeso/oogeso/context:python"><img src="https://img.shields.io/lgtm/grade/python/g/oogeso/oogeso.svg?logo=lgtm&logoWidth=18"></a>\n<a href="https://mybinder.org/v2/git/https%3A%2F%2Fbitbucket.org%2Fharald_g_svendsen%2Foogeso/HEAD?filepath=examples"><img src="https://mybinder.org/badge_logo.svg"></a>\n</p>\n<br/>\n\n# Offshore Oil and Gas Energy System Operational Optimisation Model (oogeso)\n\nPython module for modelling and analysing the energy system of offshore oil and gas fields, with renewable energy and storage integration.\n\nPart of the [Low Emission Centre](https://www.sintef.no/en/projects/lowemission-research-centre/) (SP5).\n\n## Getting started\n\nPypi distribution to come. See local installation below.\n\n## Local installation\nPrerequisite: [Poetry](https://python-poetry.org/docs/#installation)\n\nClone or download the code and install it as a python package. I.e. navigate to the folder with the MANIFEST.in file and type:\n\n### Install as a package for normal use:\n1. `poetry install`\n\n### Install dependencies for local development\n2. `poetry install --no-root`  --no-root to not install the package itself, only the dependencies.\n3. `poetry shell`\n4. `poetry run pytests tests`\n\n### Local development in Docker\nAlternatively you can run and develop the code using docker and the Dockerfile in the root folder.\n\n## User guide\nThe online user guide  gives more information about how to\nspecify input data and run a simulation case.\n\n*  [User guide](userguide.md)\n\nThere is also a (not always up-to-date) manual with more information and explanations\nabout the modelling concepts and model elements:\n\n* [Manual (pdf)](../../raw/master/doc/oogeso_manual.pdf)\n\n## Examples\nCheck out the examples:\n\n* [Simple test case](examples/test case2.ipynb?viewer=nbviewer)\n* [Test oil and gas platform](examples/TestPlatform.ipynb?viewer=nbviewer)\n\n## GitHub Actions Pipelines\n3 pipelines are defined.\n\n1. Build: Building and testing on multiple OS and python versions. Triggered on any push to GitHub.\n2. Release: Create release based on tags starting on v*.\n3. Publish: Publish package to PyPi.\n\n## Contribute\nYou are welcome to contribute to the improvement of the code.\n\n* Use Issues to describe and track needed improvements and bug fixes\n* Use branches to avoid messing things up -- but don\'t veer too far away from the trunk (master branch)\n\n### Contact\n\n[Harald G Svendsen](https://www.sintef.no/en/all-employees/employee/?empid=3414)  \nSINTEF Energy Research\n',
    'author': 'Harald Svendsen',
    'author_email': 'harald.svendsen@sintef.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oogeso/oogeso',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)

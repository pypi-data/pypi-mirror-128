# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygot',
 'pygot.api',
 'pygot.api.resources',
 'pygot.api.settings',
 'pygot.models']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.14.0,<4.0.0', 'simple-rest-client>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'pygot',
    'version': '0.2.0',
    'description': 'A Python library for https://anapioficeandfire.com',
    'long_description': '# pygot\n\nA Python library for [https://anapioficeandfire.com](https://anapioficeandfire.com)\n\n<!-- [![Github Actions Status](https://github.com/ernane/pygot/workflows/main-workflow/badge.svg)](https://github.com/ernane/pygot/actions) [![Coverage Status](https://codecov.io/gh/ernane/pygot/branch/master/graph/badge.svg)](https://codecov.io/gh/ernane/pygot) [![Code Climate](https://codeclimate.com/github/ernane/pygot/badges/gpa.svg)](https://codeclimate.com/github/ernane/pygot) [![Requirements Status](https://requires.io/github/ernane/pygot/requirements.svg?branch=master)](https://requires.io/github/ernane/pygot/requirements/?branch=master) -->\n',
    'author': 'Ernane Sena',
    'author_email': 'ernane.sena@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ernane/pygot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

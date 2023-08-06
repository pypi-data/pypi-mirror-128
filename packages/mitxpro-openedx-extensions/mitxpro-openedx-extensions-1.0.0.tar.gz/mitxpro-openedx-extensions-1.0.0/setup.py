# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitxpro_core', 'mitxpro_core.settings']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.1,<4.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['futures==3.2.0']}

entry_points = \
{'lms.djangoapp': ['mitxpro_core = mitxpro_core.apps:MITxProCoreConfig']}

setup_kwargs = {
    'name': 'mitxpro-openedx-extensions',
    'version': '1.0.0',
    'description': 'MIT xPro plugins for Open edX',
    'long_description': None,
    'author': 'MIT Office of Open Learning',
    'author_email': 'mitx-devops@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)

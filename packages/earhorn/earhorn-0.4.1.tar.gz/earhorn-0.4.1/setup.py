# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['earhorn']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'loguru>=0.5.3,<0.6.0', 'more-itertools>=8.10.0,<9.0.0']

entry_points = \
{'console_scripts': ['earhorn = earhorn.cli:run']}

setup_kwargs = {
    'name': 'earhorn',
    'version': '0.4.1',
    'description': 'Listen, monitor and archive your streams!',
    'long_description': '# earhorn\n\nListen, monitor and archive your streams!\n',
    'author': 'Joola',
    'author_email': 'jooola@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

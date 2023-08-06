# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokei_pie']

package_data = \
{'': ['*']}

install_requires = \
['plotly>=5.4.0,<6.0.0']

entry_points = \
{'console_scripts': ['tokei-pie = tokei_pie.main:main']}

setup_kwargs = {
    'name': 'tokei-pie',
    'version': '1.1.0',
    'description': 'Draw a pie chart for tokei output.',
    'long_description': '# tokei-pie\n\nRender [tokei](https://github.com/XAMPPRocky/tokei) results to charts. 🦄\n\n<a href="https://badge.fury.io/py/tokei-pie"><img src="https://badge.fury.io/py/tokei-pie.svg" alt="PyPI version"></a>\n<img src="https://badgen.net/badge/python/3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9/" alt="Python version">\n\n## Installation\n\n```shell\npip install tokei-pie\n```\n\n## Usage\n\n```shell\n$ tokei -o json | tokei-pie\n```\n\n🪄\n\n![](./docs/tokei-pie-demo.png)\n\n(This is how [django](https://github.com/django/django) looks like!)\n',
    'author': 'laixintao',
    'author_email': 'laixintaoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

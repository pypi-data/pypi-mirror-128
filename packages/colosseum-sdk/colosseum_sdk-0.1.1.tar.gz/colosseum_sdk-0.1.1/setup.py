# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.4,<2.0.0']

setup_kwargs = {
    'name': 'colosseum-sdk',
    'version': '0.1.1',
    'description': "Colosseum's SDK for developing agents",
    'long_description': '# Python3 Colosseum Agent SDK\n\n# LICENSE\n\nSee [LICENSE](LICENSE).\n',
    'author': 'h3nnn4n',
    'author_email': 'colosseum@h3nnn4n.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.colosseum.website/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)

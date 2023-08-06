# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aisexplorer']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'aisexplorer',
    'version': '0.0.1',
    'description': 'Wrapper to fetch data from marinetraffic.com',
    'long_description': 'AIS-Explorer\n############\n\nInstall\n=======\n\n>>> pip install ais_explorer\n\n\nGetting started\n===============\n\nGet Location by MMIS\n--------------------\n::\n\nimport\n\n\n',
    'author': 'reyemb',
    'author_email': 'reyemb.coding@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reyemb/AISExplorer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

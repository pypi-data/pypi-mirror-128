# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carnival', 'carnival.cmd']

package_data = \
{'': ['*']}

install_requires = \
['Click==8.0.3',
 'Fabric==2.6.0',
 'Jinja2==3.0.3',
 'invoke==1.6.0',
 'patchwork==1.0.1',
 'python-dotenv==0.19.2']

entry_points = \
{'console_scripts': ['carnival = carnival.cli:main']}

setup_kwargs = {
    'name': 'carnival',
    'version': '2.0.0',
    'description': 'Fabric-based software provisioning tool',
    'long_description': None,
    'author': 'Dmirty Simonov',
    'author_email': 'demalf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

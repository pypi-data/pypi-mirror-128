# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genurl']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=9.8.2,<10.0.0',
 'PyYAML>=6.0,<7.0',
 'Random-Word>=1.0.7,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['genurl = genurl.genurl:main']}

setup_kwargs = {
    'name': 'genurl',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sam Havens',
    'author_email': 'sam.havens@writer.com',
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

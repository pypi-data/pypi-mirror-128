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
    'version': '0.2.2',
    'description': 'GENerate random URLs',
    'long_description': "# genurl\n\n![general](https://media.giphy.com/media/JmgKSCrKZ228fIJoqt/giphy.gif)\n\nGENerate URLs\n\nThis is a sketch of how this should work. Maybe better to use a LM than some random packages, but it is funny.\n\nNOTE because this uses `/usr/share/dict/words` it may not work on all systems, and 100% won't work on Windows.\n\n## Usage\n\n```sh\n$ pip install genurl\n>>> installation output\n$ genurl\n>>> generate 1000 urls in the file urls.txt\n```\n\nYou can specify `--number` of URLs to generate and the `--outfile` path.\n\nYou can also specify `--slow` if you want, to get more word diversity at the expense of going slower.\n\n## Development\n\nmake changes, `poetry run genurl`\n\n## Publishing\n\nHaven't automated yet. First increment version in `pyproject.toml` and then `poetry publish --username PYPI_USERNAME --password PYPI_PASS --build`\n",
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

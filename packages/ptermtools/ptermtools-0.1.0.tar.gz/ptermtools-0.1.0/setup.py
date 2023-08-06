# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['git_repo_organizer']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.55,<2.0',
 'click8>=8.0.1,<9.0.0',
 'docker>=5.0.3,<6.0.0',
 'fs>=2.4.14,<3.0.0',
 'python-gitlab>=2.10.1,<3.0.0',
 'spython>=0.1.17,<0.2.0']

setup_kwargs = {
    'name': 'ptermtools',
    'version': '0.1.0',
    'description': "pgierz's organizational tools",
    'long_description': None,
    'author': 'Paul Gierz',
    'author_email': 'paulgierz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

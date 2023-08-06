# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jenkins_tui',
 'jenkins_tui.client',
 'jenkins_tui.renderables',
 'jenkins_tui.views',
 'jenkins_tui.widgets']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'dependency-injector>=4.36.2,<5.0.0',
 'httpx>=0.19.0,<0.20.0',
 'pyfiglet>=0.8.post1,<0.9',
 'rich>=10.11.0,<11.0.0',
 'textual-inputs>=0.1.2,<0.2.0',
 'textual>=0.1.12,<0.2.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['jenkins = jenkins_tui.app:run']}

setup_kwargs = {
    'name': 'jenkins-tui',
    'version': '0.1.4',
    'description': 'An interactive TUI for Jenkins',
    'long_description': None,
    'author': 'chelnak',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chelnak/jenkins-tui',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['switchconfig']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'arrow>=1.1.1,<2.0.0',
 'hier-config>=2.1.0,<3.0.0',
 'ipdb>=0.13.9,<0.14.0',
 'paramiko>=2.7.2,<3.0.0',
 'pexpect>=4.8.0,<5.0.0',
 'prompt-toolkit>=3.0.19,<4.0.0',
 'pydantic',
 'rich>=10.7.0,<11.0.0',
 'utsc.core>=0.6.0']

entry_points = \
{'console_scripts': ['utsc.switchconfig = utsc.switchconfig.__main__:cli']}

setup_kwargs = {
    'name': 'utsc.switchconfig',
    'version': '0.2.0',
    'description': 'A tool to easily provision switches on the bench',
    'long_description': None,
    'author': 'Alex Tremblay',
    'author_email': 'alex.tremblay@utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

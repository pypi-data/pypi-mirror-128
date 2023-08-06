# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloud_time_saver', 'cloud_time_saver.app']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.19.7', 'click==8.0.3', 'colorama==0.4.4', 'fire==0.4.0']

entry_points = \
{'console_scripts': ['cloud_time_saver = cloud_time_saver.cts:main']}

setup_kwargs = {
    'name': 'cloud-time-saver',
    'version': '0.1.6',
    'description': 'Python CLI tool that automates working on AWS enviorment without leaving the Terminal.',
    'long_description': None,
    'author': 'Marko Mandic',
    'author_email': 'mandicm223@gmail.com',
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

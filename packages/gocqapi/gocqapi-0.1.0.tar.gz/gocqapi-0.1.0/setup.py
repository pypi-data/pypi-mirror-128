# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gocqapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gocqapi',
    'version': '0.1.0',
    'description': 'go-cqhttp API typing annoations, return data models and utils for nonebot',
    'long_description': None,
    'author': '风屿',
    'author_email': 'i@windis.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.3,<3.10',
}


setup(**setup_kwargs)

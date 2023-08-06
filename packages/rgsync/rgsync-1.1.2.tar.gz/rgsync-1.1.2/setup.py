# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rgsync', 'rgsync.Connectors']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.3.24', 'pymongo>=3.12.0,<4.0.0', 'redis==3.5.3']

setup_kwargs = {
    'name': 'rgsync',
    'version': '1.1.2',
    'description': 'RedisGears synchronization recipe',
    'long_description': None,
    'author': 'Redis OSS',
    'author_email': 'oss@redis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

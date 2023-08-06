# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafka_connect_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'kafka-connect-api',
    'version': '0.1.0',
    'description': 'Python Client to interact with Apache Kafka Connect cluster',
    'long_description': None,
    'author': 'John Preston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

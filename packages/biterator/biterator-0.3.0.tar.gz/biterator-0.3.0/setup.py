# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biterator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'biterator',
    'version': '0.3.0',
    'description': 'Bit manipulation and iteration tool suite.',
    'long_description': '',
    'author': 'derek-strasters',
    'author_email': 'paracite.org@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

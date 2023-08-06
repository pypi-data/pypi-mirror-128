# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itm_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'itm-core',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Булыгин Евгений Андреевич',
    'author_email': 'ebulygin@ussc.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

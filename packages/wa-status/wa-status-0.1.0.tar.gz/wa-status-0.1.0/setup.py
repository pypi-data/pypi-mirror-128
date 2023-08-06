# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wa_status']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wa-status',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ggzor',
    'author_email': '30713864+ggzor@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)

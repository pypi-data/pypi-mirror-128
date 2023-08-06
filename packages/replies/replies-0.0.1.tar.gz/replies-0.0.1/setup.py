# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['replies']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'replies',
    'version': '0.0.1',
    'description': 'Composable, pure, immutable toolkit for HTTP APIs',
    'long_description': 'Serve\n=====\n\nFunctional, composable web toolkit\n',
    'author': 'Arie Bovenberg',
    'author_email': 'a.c.bovenberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

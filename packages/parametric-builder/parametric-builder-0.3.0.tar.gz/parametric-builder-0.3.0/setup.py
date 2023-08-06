# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parametric_builder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'parametric-builder',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Bidimpata-Kerim Ntumba Tshimanga',
    'author_email': 'bk.tshimanga@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unu_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'unu-api',
    'version': '0.2.2',
    'description': 'Библиотека для интеграции с биржой микрозадач unu.im',
    'long_description': None,
    'author': 'Egorov Egor',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

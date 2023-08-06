# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['izaber_zerp']

package_data = \
{'': ['*']}

install_requires = \
['izaber>=2.20210919', 'pytz>=2014.4']

setup_kwargs = {
    'name': 'izaber-zerp',
    'version': '2.0.20211119',
    'description': 'Old style izaber.zerp connectivity',
    'long_description': None,
    'author': 'Aki Mimoto',
    'author_email': 'aki@zaber.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0',
}


setup(**setup_kwargs)

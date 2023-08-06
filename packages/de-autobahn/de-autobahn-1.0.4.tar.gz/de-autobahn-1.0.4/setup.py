# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deutschland',
 'deutschland.autobahn',
 'deutschland.autobahn.api',
 'deutschland.autobahn.apis',
 'deutschland.autobahn.model',
 'deutschland.autobahn.models']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil', 'urllib3>=1.25.3']

setup_kwargs = {
    'name': 'de-autobahn',
    'version': '1.0.4',
    'description': 'Autobahn App API',
    'long_description': None,
    'author': 'BundesAPI',
    'author_email': 'kontakt@bund.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bundesAPI/autobahn-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

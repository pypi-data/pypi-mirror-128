# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hungarian_stemmer']

package_data = \
{'': ['*']}

install_requires = \
['cyhunspell>=2.0.2,<3.0.0', 'importlib-resources>=5.4.0,<6.0.0']

setup_kwargs = {
    'name': 'hungarian-stemmer',
    'version': '2021.1',
    'description': 'Hungarian stemmer package to perform higher quality stemming in Hungarian.',
    'long_description': None,
    'author': 'MONTANA Knowledge Management Ltd.',
    'author_email': 'info@distiller.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)

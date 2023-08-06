# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_data_viewer']

package_data = \
{'': ['*'], 'sphinx_data_viewer': ['assets/*']}

extras_require = \
{':extra == "docs"': ['sphinx>=4,<5']}

setup_kwargs = {
    'name': 'sphinx-data-viewer',
    'version': '0.1.0',
    'description': 'Sphinx extension to show dta in an interacitve list view',
    'long_description': None,
    'author': 'team useblocks',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

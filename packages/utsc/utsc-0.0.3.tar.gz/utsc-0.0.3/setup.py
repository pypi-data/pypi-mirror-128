# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['__main__']
install_requires = \
['loguru', 'typer']

entry_points = \
{'console_scripts': ['utsc = utsc.__main__:cli']}

setup_kwargs = {
    'name': 'utsc',
    'version': '0.0.3',
    'description': 'Root package for the utsc namespace of python packages. This package only provides the `utsc` command line tool as a namespaced wrapper around all the other `utsc.*` packages',
    'long_description': None,
    'author': 'Alex Tremblay',
    'author_email': 'alex.tremblay@utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

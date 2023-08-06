# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pydantic_secret_decimal']
install_requires = \
['pydantic>=1.8,<2.0']

setup_kwargs = {
    'name': 'pydantic-secret-decimal',
    'version': '0.1.0',
    'description': 'Secret field for Decimal types in Pydantic',
    'long_description': '# pydantic-secret-decimal\n',
    'author': 'Daniele Esposti',
    'author_email': 'daniele.esposti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/expobrain/pydantic-secret-decimal',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)

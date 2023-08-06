# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pydantic_secret_decimal']
install_requires = \
['pydantic>=1.8,<2.0']

setup_kwargs = {
    'name': 'pydantic-secret-decimal',
    'version': '0.1.2',
    'description': 'Secret field for Decimal types in Pydantic',
    'long_description': "# pydantic-secret-decimal\n\n![example branch parameter](https://github.com/expobrain/pydantic-secret-decimal/actions/workflows/main.yml/badge.svg?branch=master)\n\nThis package provides a Pydantic field `SecretDecimal` to store Decimal types as secret the same as the Pydantic's standard `SecretStr` and `SecretBytes` fields (see the [official docs](https://pydantic-docs.helpmanual.io/usage/types/#secret-types)).\n\nAn use case for the `SecretDecimal` is when storing latitude and longitude of an user which is considered as PII.\n",
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

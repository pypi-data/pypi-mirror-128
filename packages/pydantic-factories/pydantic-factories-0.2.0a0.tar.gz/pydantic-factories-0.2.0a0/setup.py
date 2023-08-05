# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_factories', 'pydantic_factories.constraints']

package_data = \
{'': ['*']}

install_requires = \
['exrex', 'faker', 'pydantic', 'typing-extensions']

setup_kwargs = {
    'name': 'pydantic-factories',
    'version': '0.2.0a0',
    'description': 'Easy data mocking and fixture generation for pydantic based models',
    'long_description': '[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_pydantic-factories&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Goldziher_pydantic-factories)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_pydantic-factories&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Goldziher_pydantic-factories)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_pydantic-factories&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=Goldziher_pydantic-factories)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_pydantic-factories&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Goldziher_pydantic-factories)\n\n# Pydantic Factories\n\nComing soon to a pypi near you\n',
    'author': "Na'aman Hirschfeld",
    'author_email': 'Naaman.Hirschfeld@sprylab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Goldziher/pydantic-factories',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

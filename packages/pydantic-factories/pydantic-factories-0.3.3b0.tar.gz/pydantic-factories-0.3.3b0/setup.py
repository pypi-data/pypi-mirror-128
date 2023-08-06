# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_factories',
 'pydantic_factories.constraints',
 'pydantic_factories.value_generators']

package_data = \
{'': ['*']}

install_requires = \
['exrex', 'faker', 'pydantic', 'typing-extensions']

setup_kwargs = {
    'name': 'pydantic-factories',
    'version': '0.3.3b0',
    'description': 'Mock data generation for pydantic based models',
    'long_description': "![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydantic-factories)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_pydantic-factories&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Goldziher_pydantic-factories)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_pydantic-factories&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Goldziher_pydantic-factories)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_pydantic-factories&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=Goldziher_pydantic-factories)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_pydantic-factories&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Goldziher_pydantic-factories)\n\n# Pydantic Factories\n\nThis library offers mock data generation for pydantic based models. This means any user defined models as well as third\nparty libraries that use pydantic as a foundation, e.g. SQLModel, FastAPI, Beanie, Ormar and others.\n\n### Features\n\n* ✅ supports both built-in and pydantic types\n* ✅ supports pydantic field constraints\n* ✅ supports complex field typings\n* ✅ supports custom model fields\n\n### Why This Library?\n\n* 💯 powerful mock data generation\n* 💯 simple to use and extend\n* 💯 rigorously tested\n\n## Installation\n\n```sh\npip install pydantic-factories\n```\n\nOR\n\n```sh\npoetry add --dev pydantic-factories\n```\n\n## Usage\n\n```python\nfrom datetime import date, datetime\nfrom typing import List, Union\n\nfrom pydantic import BaseModel, UUID4\n\nfrom pydantic_factories.factory import ModelFactory\n\n\nclass Person(BaseModel):\n    id: UUID4\n    name: str\n    hobbies: List[str]\n    age: Union[float, int]\n    birthday: Union[datetime, date]\n\n\nclass PersonFactoryWithDefaults(ModelFactory):\n    __model__ = Person\n\n\nresult = PersonFactoryWithDefaults.build()\n```\n\nThat's it - the factory will create a data object that fits the defined model and pass it to the pydantic model as\nkwargs. It will then pass through the pydantic validation and parsing mechanism, and create a model instance.\n",
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

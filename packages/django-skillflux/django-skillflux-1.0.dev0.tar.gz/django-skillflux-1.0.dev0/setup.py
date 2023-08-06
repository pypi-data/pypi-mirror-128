# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skillflux', 'skillflux.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0,<4.0']

setup_kwargs = {
    'name': 'django-skillflux',
    'version': '1.0.dev0',
    'description': 'SkillFlux — Data model and logic',
    'long_description': 'SkillFlux — Data model and logic\n================================\n\nSynopsis\n--------\n\nThis is a Django application encapsulating the SkillFlux method as\ndata model and accompanying logic. It is designed to be reusable in\nprojects that intend to employ the SkillFlux method, and are creating\ndigital tooling to support it.\n\nSkillFlux and information science\n---------------------------------\n\nTBA.\n',
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://skillflux.vision',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

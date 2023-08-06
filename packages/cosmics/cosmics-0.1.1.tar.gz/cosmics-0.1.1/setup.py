# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmics',
 'cosmics.domain',
 'cosmics.repository',
 'cosmics.repository.postgresql',
 'cosmics.service_layer',
 'cosmics.testing',
 'cosmics.testing.fakes',
 'cosmics.testing.fakes.domain',
 'cosmics.testing.fakes.repository',
 'cosmics.testing.fakes.repository.postgresql',
 'cosmics.testing.fakes.service_layer']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.9.1,<3.0.0']

extras_require = \
{'flakehell': ['flakehell>=0.8.0,<0.9.0',
               'flake8>=3.9.2,<4.0.0',
               'flake8-bandit>=2.1.2,<3.0.0',
               'flake8-blind-except>=0.2.0,<0.3.0',
               'flake8-builtins-unleashed>=1.3.1,<2.0.0',
               'flake8-bugbear>=20.11.1,<21.0.0',
               'flake8-comprehensions>=3.3.1,<4.0.0',
               'flake8-debugger>=4.0.0,<5.0.0',
               'flake8-docstrings>=1.5.0,<2.0.0',
               'flake8-eradicate>=1.0.0,<2.0.0',
               'flake8-mutable>=1.2.0,<2.0.0',
               'flake8-pytest-style>=1.3.0,<2.0.0',
               'flake8-simplify>=0.14.2,<0.15.0',
               'pep8-naming>=0.11.1,<0.12.0',
               'pydocstyle>=5.1.1,<6.0.0',
               'pyflakes>=2.3.0,<2.4.0']}

setup_kwargs = {
    'name': 'cosmics',
    'version': '0.1.1',
    'description': 'Tools for an event-driven design following Cosmic Python',
    'long_description': '# cosmics\n[![pipeline status](https://gitlab.com/emmerich-os/cosmics/badges/main/pipeline.svg)](https://gitlab.com/emmerich-os/cosmics/-/commits/main)\n[![coverage report](https://gitlab.com/emmerich-os/cosmics/badges/main/coverage.svg)](https://gitlab.com/emmerich-os/cosmics/-/commits/main)\n[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA set of helper classes suitable for an event-driven software design. Inspired by the Cosmic Python book.\n\nThe API documentation can be found [here](https://emmerich-os.gitlab.io/cosmics).\n\n## Helper Classes\n\n- Repository as a database inferface.\n- Client for interaction between repository and database. Allows to decouple the repository from the database type.\n- Messagebus for forwarding commands and events to their respective handler functions.\n- Unit of Work for processing commands/events with(-out) database access.\n',
    'author': 'Fabian Emmerich',
    'author_email': 'gitlab@emmerichs.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/emmerich-os/cosmics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

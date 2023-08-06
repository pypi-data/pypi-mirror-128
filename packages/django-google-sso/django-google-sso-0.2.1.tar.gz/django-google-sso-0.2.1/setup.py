# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_google_sso', 'django_google_sso.migrations', 'django_google_sso.tests']

package_data = \
{'': ['*'], 'django_google_sso': ['templates/admin_sso/*']}

install_requires = \
['django',
 'google-auth',
 'google-auth-httplib2',
 'google-auth-oauthlib',
 'loguru']

setup_kwargs = {
    'name': 'django-google-sso',
    'version': '0.2.1',
    'description': 'Easily add Google SSO login to Django Admin',
    'long_description': '## Welcome to Django Google SSO\n[![PyPI](https://img.shields.io/pypi/v/django-google-sso)](https://pypi.org/project/django-google-sso/)\n[![Build](https://github.com/chrismaille/django-google-sso/workflows/tests/badge.svg)](https://github.com/chrismaille/django-google-sso/actions)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-google-sso)](https://www.python.org)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n',
    'author': 'Chris Maillefaud',
    'author_email': 'chrismaillefaud@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrismaille/django-google-sso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

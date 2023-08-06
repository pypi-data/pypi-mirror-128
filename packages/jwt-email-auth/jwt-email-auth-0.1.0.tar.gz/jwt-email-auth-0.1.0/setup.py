# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jwt_email_auth']

package_data = \
{'': ['*'], 'jwt_email_auth': ['locale/fi/LC_MESSAGES/*']}

install_requires = \
['Django>=3.2.9,<4.0.0',
 'PyJWT>=2.3.0,<3.0.0',
 'cryptography>=36.0.0,<37.0.0',
 'django-ipware>=4.0.0,<5.0.0',
 'djangorestframework>=3.12.2,<4.0.0']

setup_kwargs = {
    'name': 'jwt-email-auth',
    'version': '0.1.0',
    'description': 'JWT authentication from email login codes.',
    'long_description': "# JSON Web Token Email Authentiation\n\n[![Coverage Status](https://coveralls.io/repos/github/MrThearMan/jwt-email-auth/badge.svg?branch=main)](https://coveralls.io/github/MrThearMan/jwt-email-auth?branch=main)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/MrThearMan/jwt-email-auth/Tests)](https://github.com/MrThearMan/jwt-email-auth/actions/workflows/main.yml)\n[![PyPI](https://img.shields.io/pypi/v/jwt-email-auth)](https://pypi.org/project/jwt-email-auth)\n[![GitHub](https://img.shields.io/github/license/MrThearMan/jwt-email-auth)](https://github.com/MrThearMan/jwt-email-auth/blob/main/LICENSE)\n[![GitHub last commit](https://img.shields.io/github/last-commit/MrThearMan/jwt-email-auth)](https://github.com/MrThearMan/jwt-email-auth/commits/main)\n[![GitHub issues](https://img.shields.io/github/issues-raw/MrThearMan/jwt-email-auth)](https://github.com/MrThearMan/jwt-email-auth/issues)\n\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jwt-email-auth)](https://pypi.org/project/jwt-email-auth)\n[![PyPI - Django Version](https://img.shields.io/pypi/djversions/jwt-email-auth)](https://pypi.org/project/jwt-email-auth)\n[![Custom - Django REST Framework Version](https://img.shields.io/badge/drf%20versions-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/jwt-email-auth)\n\n```shell\npip install jwt-email-auth\n```\n---\n\n**Documentation**: [https://mrthearman.github.io/jwt-email-auth/](https://mrthearman.github.io/jwt-email-auth/)\n\n**Source Code**: [https://github.com/MrThearMan/jwt-email-auth](https://github.com/MrThearMan/jwt-email-auth)\n\n---\n\nThis module enables JSON Web Token Authentication in Django Rest framework without using Django's User model.\nInstead, login information is stored in [cache](https://docs.djangoproject.com/en/3.2/topics/cache/#the-low-level-cache-api),\na login code is sent to the user's email inbox, and then the cached information is obtained\nusing the code that was sent to the given email.\n",
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrThearMan/jwt-email-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)

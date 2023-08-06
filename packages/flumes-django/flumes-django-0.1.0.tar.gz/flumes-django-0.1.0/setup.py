# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flumes_django', 'flumes_django.templatetags', 'flumes_django.tests']

package_data = \
{'': ['*'],
 'flumes_django': ['static/admin/flume_django/common/*',
                   'templates/admin/flumes_django/file/*',
                   'templates/admin/flumes_django/info/*',
                   'templates/admin/flumes_django/stream/*',
                   'templates/flumes_django/templatetags/*']}

install_requires = \
['Django>=2.2,<4.0', 'flumes>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'flumes-django',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jorge Zapata',
    'author_email': 'jorgeluis.zapata@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jnt_django_graphene_toolbox',
 'jnt_django_graphene_toolbox.connections',
 'jnt_django_graphene_toolbox.errors',
 'jnt_django_graphene_toolbox.fields',
 'jnt_django_graphene_toolbox.filters',
 'jnt_django_graphene_toolbox.filters.mixins',
 'jnt_django_graphene_toolbox.helpers',
 'jnt_django_graphene_toolbox.mutations',
 'jnt_django_graphene_toolbox.nodes',
 'jnt_django_graphene_toolbox.types',
 'jnt_django_graphene_toolbox.views']

package_data = \
{'': ['*']}

install_requires = \
['django-filter',
 'djangorestframework',
 'graphene-file-upload',
 'graphene_django',
 'jnt_django_toolbox']

setup_kwargs = {
    'name': 'jnt-django-graphene-toolbox',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Junte',
    'author_email': 'tech@junte.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

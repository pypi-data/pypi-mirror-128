# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['the_social_network',
 'the_social_network.migrations',
 'the_social_network.serializers',
 'the_social_network.urls',
 'the_social_network.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.9,<4.0.0',
 'Pillow>=8.4.0,<9.0.0',
 'django-cors-headers>=3.10.0,<4.0.0',
 'django-dotenv>=1.4.2,<2.0.0',
 'djangorestframework>=3.12.4,<4.0.0',
 'uWSGI>=2.0.20,<3.0.0']

setup_kwargs = {
    'name': 'the-social-network',
    'version': '0.0.2',
    'description': 'Basic social network core.',
    'long_description': '# The Social Network\n\nThe package "The Social Network" is a django base backend core element for any possible social network you can think of.\n\nIt contains the following models\n\nDjango.Authentication.User\n',
    'author': 'Marc Feger',
    'author_email': 'marc.feger@hhu.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.cs.uni-duesseldorf.de/feger/the-social-network',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

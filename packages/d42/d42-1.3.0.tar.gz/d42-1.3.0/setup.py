# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d42']

package_data = \
{'': ['*']}

install_requires = \
['blahblah>=1.3,<1.4',
 'district42>=1.3,<1.4',
 'revolt>=1.3,<1.4',
 'valera>=1.3,<1.4']

setup_kwargs = {
    'name': 'd42',
    'version': '1.3.0',
    'description': '',
    'long_description': None,
    'author': 'Nikita Tsvetkov',
    'author_email': 'nikitanovosibirsk@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nikitanovosibirsk/d42',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

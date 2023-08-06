# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['variant']

package_data = \
{'': ['*']}

install_requires = \
['pyensembl>=1.9.4,<2.0.0', 'varcode']

entry_points = \
{'console_scripts': ['variant-effect = variant.effect:run']}

setup_kwargs = {
    'name': 'variant',
    'version': '0.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'Chang Ye',
    'author_email': 'yech1990@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

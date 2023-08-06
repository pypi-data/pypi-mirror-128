# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lazyds',
 'lazyds.data',
 'lazyds.evaluation',
 'lazyds.learning',
 'lazyds.learning.supervised',
 'lazyds.learning.supervised.classification']

package_data = \
{'': ['*']}

install_requires = \
['arff2pandas>=1.0.1,<2.0.0',
 'idict>=1.211123.3,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'scikit-learn>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'lazyds',
    'version': '0.211123.2',
    'description': 'Useful Data Science libraries wrapped by laziness',
    'long_description': None,
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

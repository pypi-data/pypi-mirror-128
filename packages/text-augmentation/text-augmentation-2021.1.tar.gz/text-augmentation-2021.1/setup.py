# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_augmentation']

package_data = \
{'': ['*']}

install_requires = \
['digital-twin-distiller>=2021.12,<2022.0',
 'fasttext>=0.9.2,<0.10.0',
 'gensim>=4.1.2,<5.0.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'text-augmentation',
    'version': '2021.1',
    'description': 'Package to perform text augmentation.',
    'long_description': None,
    'author': 'MONTANA Knowledge Management ltd.',
    'author_email': 'info@distiller.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

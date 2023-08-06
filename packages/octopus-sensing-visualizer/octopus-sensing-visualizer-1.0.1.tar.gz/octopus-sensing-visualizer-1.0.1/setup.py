# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octopus_sensing_visualizer', 'octopus_sensing_visualizer.prepare_data']

package_data = \
{'': ['*']}

install_requires = \
['CherryPy>=18.6.0,<19.0.0',
 'heartpy>=1.2.7,<2.0.0',
 'neurokit>=0.2.0,<0.3.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.2.5,<2.0.0',
 'pycairo>=1.20.1,<2.0.0']

setup_kwargs = {
    'name': 'octopus-sensing-visualizer',
    'version': '1.0.1',
    'description': 'Library for visualizing data synchronously recorded from different sensors',
    'long_description': None,
    'author': 'Nastaran Saffaryazdi',
    'author_email': 'nsaffar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://octopus-sensing.nastaran-saffar.me',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

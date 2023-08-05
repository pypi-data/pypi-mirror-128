# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyobs_gui', 'pyobs_gui.qt']

package_data = \
{'': ['*'], 'pyobs_gui.qt': ['resources/*']}

install_requires = \
['PyQt5>=5.13,<6.0',
 'colour>=0.1,<0.2',
 'matplotlib>=3.4,<4.0',
 'qfitswidget>=0.8,<0.9']

setup_kwargs = {
    'name': 'pyobs-gui',
    'version': '0.14.1',
    'description': 'A remote GUI for pyobs',
    'long_description': None,
    'author': 'Tim-Oliver Husser',
    'author_email': 'thusser@uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

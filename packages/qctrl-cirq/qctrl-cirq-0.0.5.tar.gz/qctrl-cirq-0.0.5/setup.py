# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlcirq']

package_data = \
{'': ['*']}

install_requires = \
['cirq>=0.6.0,<0.7.0',
 'numpy>=1.16,<2.0',
 'qctrl-open-controls>=8.5.1,<9.0.0',
 'scipy>=1.3,<2.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'qctrl-cirq',
    'version': '0.0.5',
    'description': 'Q-CTRL Python Cirq',
    'long_description': '# Q-CTRL Python Cirq\n\nThe aim of the Q-CTRL Cirq Adapter package is to provide export functions allowing\nusers to deploy established error-robust quantum control protocols from the\nopen literature and defined in Q-CTRL Open Controls on Google quantum devices\nand simulators.\n\nAnyone interested in quantum control is welcome to contribute to this project.',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)

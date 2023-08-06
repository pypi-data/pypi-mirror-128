# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlqiskit']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0',
 'qctrl-open-controls>=8.5.1,<9.0.0',
 'qiskit-ibmq-provider>=0.3.3,<0.4.0',
 'qiskit-terra>=0.12.0,<0.13.0',
 'scipy>=1.3,<2.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'qctrl-qiskit',
    'version': '0.0.4',
    'description': 'Q-CTRL Qiskit Adapter',
    'long_description': '# Q-CTRL Qiskit adapter\n\nThe aim of the Q-CTRL Qiskit Adapter package is to provide export functions allowing\nusers to deploy established error-robust quantum control protocols from the\nopen literature and defined in Q-CTRL Open Controls on IBM Quantum hardware.\n\nAnyone interested in quantum control is welcome to contribute to this project.\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qctrl/python-qiskit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)

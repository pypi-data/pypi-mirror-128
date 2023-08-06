# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netdata']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<1', 'yarl>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'netdata',
    'version': '1.0.1',
    'description': 'Python API for interacting with Netdata',
    'long_description': 'python-netdata\n==============\n\nPython API for interacting with `Netdata <https://my-netdata.io/>`_. Currently\nare the ``data``, the ``allmetrics`` and the ``alarms`` endpoint supported.\n\nThis module is not official, developed, supported or endorsed by Netdata.\n\nInstallation\n------------\n\nThe module is available from the `Python Package Index <https://pypi.python.org/pypi>`_.\n\n.. code:: bash\n\n    $ pip3 install netdata\n\nOn a Fedora-based system or on a CentOS/RHEL machine which has EPEL enabled.\n\n.. code:: bash\n\n    $ sudo dnf -y install python3-netdata\n\nFor Nix or NixOS users is a package available. Keep in mind that the lastest releases might only\nbe present in the ``unstable`` channel.\n\n.. code:: bash\n\n    $ nix-env -iA nixos.python39Packages.netdata\n\nUsage\n-----\n\nThe file ``example.py`` contains an example about how to use this module.\n\nDevelopment\n-----------\n\nFor development is recommended to use a ``venv``.\n\n.. code:: bash\n\n    $ python3 -m venv .\n    $ source bin/activate\n    $ python3 setup.py develop\n\nLicense\n-------\n\n``python-netdata`` is licensed under MIT, for more details check LICENSE.\n',
    'author': 'Fabian Affolter',
    'author_email': 'mail@fabian-affolter.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/home-assistant-ecosystem/python-netdata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

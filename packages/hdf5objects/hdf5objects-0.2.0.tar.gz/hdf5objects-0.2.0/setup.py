# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hdf5objects',
 'hdf5objects.dataframes',
 'hdf5objects.datasets',
 'hdf5objects.datasets.axes',
 'hdf5objects.fileobjects',
 'hdf5objects.xltek',
 'hdf5objects.xltek.ui',
 'hdf5objects.xltek.ultity']

package_data = \
{'': ['*']}

install_requires = \
['baseobjects>=1.5.2,<2.0.0',
 'bidict>=0.21.3,<0.22.0',
 'classversioning>=0.4.1,<0.5.0',
 'dspobjects>=0.1.0,<0.2.0',
 'framestructure>=0.3.0,<0.4.0',
 'h5py>=3.5.0,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pytz>=2021.1,<2022.0',
 'tzlocal>=3.0,<4.0']

entry_points = \
{'console_scripts': ['hdf5objects = hdf5objects.__main__:main']}

setup_kwargs = {
    'name': 'hdf5objects',
    'version': '0.2.0',
    'description': 'hdf5objects',
    'long_description': "hdf5objects\n===========\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/hdf5objects.svg\n   :target: https://pypi.org/project/hdf5objects/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/hdf5objects.svg\n   :target: https://pypi.org/project/hdf5objects/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/hdf5objects\n   :target: https://pypi.org/project/hdf5objects\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/hdf5objects\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/hdf5objects/latest.svg?label=Read%20the%20Docs\n   :target: https://hdf5objects.readthedocs.io/\n   :alt: Read the documentation at https://hdf5objects.readthedocs.io/\n.. |Tests| image:: https://github.com/FongAnthonyM/hdf5objects/workflows/Tests/badge.svg\n   :target: https://github.com/FongAnthonyM/hdf5objects/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/FongAnthonyM/hdf5objects/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/FongAnthonyM/hdf5objects\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *hdf5objects* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install hdf5objects\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*hdf5objects* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/FongAnthonyM/hdf5objects/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://hdf5objects.readthedocs.io/en/latest/usage.html\n",
    'author': 'Anthony Fong',
    'author_email': 'FongAnthonyM@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/FongAnthonyM/hdf5objects',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pysmooth']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'hypothesis>=6.27.1,<7.0.0',
 'nox-poetry>=0.9.0,<0.10.0',
 'numpy>=1.21.4,<2.0.0',
 'rich>=10.14.0,<11.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['pysmooth = pysmooth.__main__:main']}

setup_kwargs = {
    'name': 'pysmooth',
    'version': '1.0.1',
    'description': "Pysmooth: a Python implementation of R's stats::smooth Tukey's (running median) smoother",
    'long_description': "Pysmooth\n==========\n\nA Python implementation of R's stats::smooth() Tukey's (running median) smoother\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/pysmooth.svg\n   :target: https://pypi.org/project/pysmooth/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/pysmooth.svg\n   :target: https://pypi.org/project/pysmooth/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pysmooth\n   :target: https://pypi.org/project/pysmooth\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/pysmooth\n   :target: https://opensource.org/licenses/GPL-3.0\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/pysmooth/latest.svg?label=Read%20the%20Docs\n   :target: https://pysmooth.readthedocs.io/\n   :alt: Read the documentation at https://pysmooth.readthedocs.io/\n.. |Tests| image:: https://github.com/mcsmith/pysmooth/workflows/Tests/badge.svg\n   :target: https://github.com/mcsmith/pysmooth/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/mcsmith/pysmooth/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/mcsmith/pysmooth\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n  - Replace code C/R-style coding with more Pythonic methods\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Pysmooth* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install pysmooth\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `GPL 3.0 license`_,\n*Pysmooth* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _GPL 3.0 license: https://opensource.org/licenses/GPL-3.0\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/mcsmith/pysmooth/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://pysmooth.readthedocs.io/en/latest/usage.html\n",
    'author': 'Miles Smith',
    'author_email': 'mileschristiansmith@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcsmith/pysmooth',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)

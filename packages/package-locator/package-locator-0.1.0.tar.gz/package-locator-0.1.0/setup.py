# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package_locator']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.0,<9.0.0',
 'giturlparse>=0.10.0,<0.11.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.3.0,<11.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['package-locator = package_locator.__main__:main']}

setup_kwargs = {
    'name': 'package-locator',
    'version': '0.1.0',
    'description': 'For a package, locate its source repository url and its relative path within the repository',
    'long_description': 'package-locator\n===========================\n\n|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov| |pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/package-locator.svg\n   :target: https://pypi.org/project/package-locator/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/package-locator\n   :target: https://pypi.org/project/package-locator\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/nasifimtiazohi/package-locator\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/package-locator/latest.svg?label=Read%20the%20Docs\n   :target: https://package-locator.readthedocs.io/\n   :alt: Read the documentation at https://package-locator.readthedocs.io/\n.. |Build| image:: https://github.com/nasifimtiazohi/package-locator/workflows/Build%20package-locator%20Package/badge.svg\n   :target: https://github.com/nasifimtiazohi/package-locator/actions?workflow=Package\n   :alt: Build Package Status\n.. |Tests| image:: https://github.com/nasifimtiazohi/package-locator/workflows/Run%20package-locator%20Tests/badge.svg\n   :target: https://github.com/nasifimtiazohi/package-locator/actions?workflow=Tests\n   :alt: Run Tests Status\n.. |Codecov| image:: https://codecov.io/gh/nasifimtiazohi/package-locator/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/nasifimtiazohi/package-locator\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *package-locator* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install package-locator\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nCredits\n-------\n\nThis package was created with cookietemple_ using Cookiecutter_ based on Hypermodern_Python_Cookiecutter_.\n\n.. _cookietemple: https://cookietemple.com\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _PyPI: https://pypi.org/\n.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _pip: https://pip.pypa.io/\n.. _Usage: https://package-locator.readthedocs.io/en/latest/usage.html\n',
    'author': 'Nasif Imtiaz',
    'author_email': 'nasifimtiaz88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nasifimtiazohi/package-locator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

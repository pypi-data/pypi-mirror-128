# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clophfit', 'clophfit.old']

package_data = \
{'': ['*'], 'clophfit.old': ['bash/*']}

install_requires = \
['arviz>=0.11.4,<0.12.0',
 'corner>=2.2.1,<3.0.0',
 'emcee>=3.1.1,<4.0.0',
 'lmfit>=0.8,<0.9',
 'numdifftools>=0.9.40,<0.10.0',
 'numpy>=1.17,<2.0',
 'pandas>=1.3.3,<2.0.0',
 'rpy2>=3.4.5,<4.0.0',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'sympy>=1.9,<2.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['clop = clophfit.cli:run']}

setup_kwargs = {
    'name': 'clophfit',
    'version': '0.3.0a1',
    'description': 'Cli for fitting macromolecule pH titration or binding assays data e.g. fluorescence spectra.',
    'long_description': '|Tests| |PyPI| |RtD|\n\nClopHfit\n========\n\n-  Cli for fitting macromolecule pH titration or binding assays data\n   e.g.\xa0fluorescence spectra.\n-  Version: “0.3.0a1”\n\n\nInstallation\n------------\n\nAt this stage few scripts are available in src/clophfit/old.\n\n::\n\n   pyenv install 3.6.15\n   poetry install\n   poetry run pytest -v\n\n\nUse\n---\n\nfit_titration.py\n~~~~~~~~~~~~~~~~\n\nA single script for pK and Cl and various methods w/out bootstraping: 1.\nsvd 2. bands and 3. single lambda.\n\n   input ← csvtable and note_file\n\n..\n\n   output → pK spK (stdout) and pdf of analysis\n\nTo do\n^^^^^\n\n-  Bootstrap svd with optimize or lmfit.\n-  **Average spectra**\n-  Join spectra [‘B’, ‘E’, ‘F’]\n-  Compute band integral (or sums)\n\nfit_titration_global.py\n~~~~~~~~~~~~~~~~~~~~~~~\n\nA script for fitting tuples (y1, y2) of values for each concentration\n(x). It uses lmfit confint and bootstrap.\n\n   input ← x y1 y2 (file)\n\n..\n\n   output → K SA1 SB1 SA2 SB2 , png and correl.png\n\n\nIn global fit the best approach was using lmfit without bootstraping.\n\nExample\n^^^^^^^\n\n::\n\n    for i in *.dat; do gfit $i png2 --boot 99 > png2/$i.txt; done\n\n\nOld tecan todo list\n-------------------\n\nI do not know how to unittest\n\n- better fit 400, 485 (also separated) e bootstrap to estimate\n  uncertanty\n\n- print sorted output\n\n- buffer correction and report controls e.g.\xa0S202N, E2 and V224Q\n\n- dilution correction\n\n- check metadata and report the diff REMEMBER 8.8; dataframe groupby\n  per meta_pre, ma anche enspire\n\n- **fit chloride**\n\n- fluorescence is constant? GREAT\n\n- plot data when fit fail and save txt file\n\n\nDevelopment\n-----------\n\nMake sure this README passes https://pypi.org/project/readme-renderer/\n\n::\n\n   gh release create (--target devel) v0.3.0a0\n\n   gh workflow disable|enable|view|run|list\n\n\nTL;DR\n~~~~~\n\n::\n\n   poetry env use 3.9\n   poetry install\n   pre-commit install\n   pre-commit install --hook-type commit-msg\n\nWhen needed (e.g. API updates)::\n\n   sphinx-apidoc -f -o docs/api/ src/clophfit/\n\nFor Jupyter_::\n\n    poetry run python -m ipykernel install --user --name="clophfit"\n\nDevelopment environment\n~~~~~~~~~~~~~~~~~~~~~~~\n\n* Test automation requires nox and nox-poetry.\n\n* Formatting with black[jupyter] configured in pyproject.\n\n* Linters are configured in .flake8 .darglint and .isort.cfg and include::\n\n  - flake8-isort\n  - flake8-bugbear\n  - flake8-docstrings\n  - darglint\n  - flake8-eradicate\n  - flake8-comprehensions\n  - flake8-pytest-style\n  - flake8-annotations (see mypy)\n\n* pre-commit configured in .pre-commit-config.yaml activated with::\n\n  - pre-commit install\n  - commitizen install --hook-type commit-msg\n\n* Tests coverage (pytest-cov) configured in .coveragerc.\n\n* Type annotation configured in mypy.ini.\n\n* Commitizen_ also used to bump version::\n\n\tcz bump --changelog --prerelease alpha --increment MINOR\n\n  * need one-time initialization::\n\n\t  (cz init)\n\n* xdoctest\n\n* sphinx with pydata-sphinx-theme and sphinx-autodoc-typehints. (nbsphinx, sphinxcontrib-plantuml)::\n\n\tmkdir docs; cd docs\n\tsphinx-quickstart\n  \n  Edit conf.py ["sphinx.ext.autodoc"] and index.rst [e.g. api/modules]::\n\n    sphinx-apidoc -f -o docs/api/ src/clophfit/\n\n* CI/CD to PYPI_ configured in .github/::\n\n\ttests.yml\n\trelease.yml\n\nWhat is missing to modernize_:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n- coveralls/Codecov\n- release drafter\n- readthedocs or ghpages?\n  https://www.docslikecode.com/articles/github-pages-python-sphinx/ \n\n\n\n\n\n.. |Tests| image:: https://github.com/darosio/ClopHfit/workflows/Tests/badge.svg\n   :target: https://github.com/darosio/ClopHfit/actions?workflow=Tests\n.. |PyPI| image:: https://img.shields.io/pypi/v/ClopHfit.svg\n   :target: https://pypi.org/project/ClopHfit/\n.. |RtD| image:: https://readthedocs.org/projects/clophfit/badge/\n   :target: https://clophfit.readthedocs.io/\n\n.. _Commitizen: https://commitizen-tools.github.io/commitizen/\n\n.. _Jupyter: https://jupyter.org/\n\n.. _modernize: https://cjolowicz.github.io/posts/hypermodern-python-06-ci-cd/\n\n.. _PYPI: https://pypi.org/project/clophfit/\n',
    'author': 'daniele arosio',
    'author_email': 'daniele.arosio@cnr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/darosio/ClopHfit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8,<3.10',
}


setup(**setup_kwargs)

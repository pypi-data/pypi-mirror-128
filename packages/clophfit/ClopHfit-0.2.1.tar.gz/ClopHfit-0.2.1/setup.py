# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clophfit', 'clophfit.old']

package_data = \
{'': ['*'], 'clophfit.old': ['bash/*']}

install_requires = \
['lmfit>=0.8,<0.9',
 'matplotlib>=1,<2',
 'numpy>=1.10,<1.11',
 'pandas>=0.18,<0.19',
 'scipy>=0.18,<0.19',
 'seaborn>=0.7,<0.8']

entry_points = \
{'console_scripts': ['fit_rpy = clophfit.fit_rpy:main']}

setup_kwargs = {
    'name': 'clophfit',
    'version': '0.2.1',
    'description': 'Cli for fitting macromolecule pH titration or binding assays data e.g. fluorescence spectra.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/ClopHfit.svg)](https://pypi.org/project/ClopHfit/)\n\n# ClopHfit #\n\n* Cli for fitting macromolecule pH titration or binding assays data e.g. fluorescence spectra.\n* Version: "0.1.1"\n\n## Installation\n\nAt this stage few scripts are available in src/clophfit/old.\n\n    pyenv install 3.6.15\n    poetry install\n    poetry run pytest -v\n\n## Use\n\n### fit_titration.py ###\n\nA single script for pK and Cl and various methods w/out bootstraping:\n1. svd\n2. bands and\n3. single lambda.\n\n>   input ← csvtable and note_file\n\n>   output → pK spK (stdout) and pdf of analysis\n\n#### To do\n\n- Bootstrap svd with optimize or lmfit.\n- **Average spectra**\n- Join spectra [\'B\', \'E\', \'F\']\n- Compute band integral (or sums)\n\n### fit_titration_global.py ###\n\nA script for fitting tuples (y1, y2) of values for each concentration (x).\nIt uses lmfit confint and bootstrap.\n\n>   input ← x y1 y2 (file)\n\n>   output → K SA1 SB1 SA2 SB2 , png and correl.png\n    \nIn global fit the best approach was using lmfit without bootstraping.\n\n#### Example\n     \n\t for i in *.dat; do gfit $i png2 --boot 99 > png2/$i.txt; done\n',
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
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

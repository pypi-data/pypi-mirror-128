# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clophfit']

package_data = \
{'': ['*'], 'clophfit': ['scripts/*']}

install_requires = \
['lmfit>=0.8,<0.9',
 'matplotlib>=1,<2',
 'numpy>=1.10,<1.11',
 'pandas>=0.18,<0.19',
 'rpy2>=2.3,<2.4',
 'scipy>=0.18,<0.19',
 'seaborn>=0.7,<0.8']

setup_kwargs = {
    'name': 'clophfit',
    'version': '0.2.0',
    'description': 'Cli for fitting macromolecule pH titration or binding assays data e.g. fluorescence spectra.',
    'long_description': '# README #\n\nThis README would normally document whatever steps are necessary to get your application up and running.\n\n### What is this repository for? ###\n\n* Quick summary\n* Version\n* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)\n\n### How do I get set up? ###\n\n* Summary of set up\n* Configuration\n* Dependencies\n* Database configuration\n* How to run tests\n* Deployment instructions\n\n### Contribution guidelines ###\n\n* Writing tests\n* Code review\n* Other guidelines\n\n### Who do I talk to? ###\n\n* Repo owner or admin\n* Other community or team contact',
    'author': 'daniele arosio',
    'author_email': 'daniele.arosio@cnr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bitbucket.org/darosio/clophfit/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

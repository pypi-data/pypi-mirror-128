# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['overreact', 'overreact.thermo']

package_data = \
{'': ['*']}

install_requires = \
['cclib>=1.6.3,<2.0.0', 'scipy>=1.7.3,<2.0.0']

extras_require = \
{'cli': ['rich>=10.12.0,<11.0.0'],
 'fast': ['jax>=0.2.24,<0.3.0', 'jaxlib>=0.1.73,<0.2.0'],
 'solvents': ['thermo>=0.2.10,<0.3.0']}

entry_points = \
{'console_scripts': ['overreact = overreact._cli:main']}

setup_kwargs = {
    'name': 'overreact',
    'version': '1.0.2',
    'description': '📈 Create and analyze chemical microkinetic models built from computational chemistry data',
    'long_description': '[![DOI](https://zenodo.org/badge/214332027.svg)](https://zenodo.org/badge/latestdoi/214332027)\n[![PyPI](https://img.shields.io/pypi/v/overreact)](https://pypi.org/project/overreact/)\n[![build](https://github.com/geem-lab/overreact/actions/workflows/python-package.yml/badge.svg)](https://github.com/geem-lab/overreact/actions/workflows/python-package.yml)\n[![codecov](https://codecov.io/gh/geem-lab/overreact/branch/main/graph/badge.svg?token=4WAVXCRXY8)](https://codecov.io/gh/geem-lab/overreact)\n[![GitHub license](https://img.shields.io/github/license/geem-lab/overreact)](https://github.com/geem-lab/overreact/blob/main/LICENSE)\n\n[![User guide](https://img.shields.io/badge/user%20guide-available-blue)](https://geem-lab.github.io/overreact-guide/)\n[![GitHub Discussions](https://img.shields.io/github/discussions/geem-lab/overreact)](https://github.com/geem-lab/overreact/discussions)\n[![GitHub issues](https://img.shields.io/github/issues-raw/geem-lab/overreact)](https://github.com/geem-lab/overreact/issues)\n[![Made in Brazil 🇧🇷](https://img.shields.io/badge/made%20in-Brazil-009c3b)](https://pypi.org/project/overreact/)\n\n<div align="center">\n    <img alt="overreact" src="https://raw.githubusercontent.com/geem-lab/overreact-guide/master/logo.png" />\n</div>\n\n**overreact** is a **library** and a **command-line tool** for building and\nanalyzing\n[microkinetic models](https://geem-lab.github.io/overreact-guide/#microkinetic).\nData is parsed directly from computational chemistry output files thanks to\n[`cclib`](https://cclib.github.io/) (see the\n[list of supported programs](https://cclib.github.io/#summary)).\n\nTake a look at the [**user guide**](https://geem-lab.github.io/overreact-guide/)\nfor more information on how to use **overreact**. Or check out the\n[**API documentation**](https://geem-lab.github.io/overreact/overreact.html) for\na more detailed description of the application programming interface.\n\n## Installation\n\n**overreact** is a Python package, so you can easily install it with\n[`pip`](https://pypi.org/project/pip/):\n\n```bash\n$ pip install "overreact[cli,fast]"\n```\n\nSee the\n[installation guide](https://geem-lab.github.io/overreact-guide/install.html)\nfor more details.\n\n## Citing **overreact**\n\nIf you use **overreact** in your research, please cite:\n\n> F. S. S. Schneider and G. F. Caramori. _**geem-lab/overreact**: a tool for\n> creating and analyzing microkinetic models built from computational chemistry\n> data, v1.0.2_. **2021**.\n> [DOI:10.5281/ZENODO.5643960](https://zenodo.org/badge/latestdoi/214332027).\n> Freely available at: <<https://github.com/geem-lab/overreact>>.\n\nHere\'s the reference in [BibTeX](http://www.bibtex.org/) format:\n\n```bibtex\n@misc{overreact2021,\n  howpublished = {\\url{https://github.com/geem-lab/overreact}}\n  year = {2021},\n  author = {Schneider, F. S. S. and Caramori, G. F.},\n  title = {\n    \\textbf{geem-lab/overreact}: a tool for creating and analyzing\n    microkinetic models built from computational chemistry data, v1.0.2\n  },\n  doi = {10.5281/ZENODO.5643960},\n  url = {https://zenodo.org/record/5643960},\n  publisher = {Zenodo},\n  copyright = {Open Access}\n}\n```\n\nA paper describing **overreact** is currently being prepared. When it is\npublished, the above BibTeX entry will be updated.\n\n## License\n\n**overreact** is open-source, released under the permissive **MIT license**. See\n[the LICENSE agreement](https://github.com/geem-lab/overreact/blob/main/LICENSE).\n\n## Funding\n\nThis project was developed at the [GEEM lab](https://geem-ufsc.org/)\n([Federal University of Santa Catarina](https://en.ufsc.br/), Brazil), and was\npartially funded by the\n[Brazilian National Council for Scientific and Technological Development (CNPq)](https://cnpq.br/),\ngrant number 140485/2017-1.\n',
    'author': 'Felipe S. S. Schneider',
    'author_email': 'schneider.felipe@posgrad.ufsc.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://geem-lab.github.io/overreact-guide/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

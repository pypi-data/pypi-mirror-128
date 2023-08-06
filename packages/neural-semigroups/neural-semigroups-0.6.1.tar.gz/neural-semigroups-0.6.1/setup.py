# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neural_semigroups']

package_data = \
{'': ['*']}

install_requires = \
['pytorch-ignite', 'tensorboard', 'torch', 'tqdm']

setup_kwargs = {
    'name': 'neural-semigroups',
    'version': '0.6.1',
    'description': 'Neural networks powered research of semigroups',
    'long_description': "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inpefess/neural-semigroups/blob/master/examples/dae_4_colab.ipynb) [![PyPI version](https://badge.fury.io/py/neural-semigroups.svg)](https://badge.fury.io/py/neural-semigroups) [![CircleCI](https://circleci.com/gh/inpefess/neural-semigroups.svg?style=svg)](https://circleci.com/gh/inpefess/neural-semigroups) [![Documentation Status](https://readthedocs.org/projects/neural-semigroups/badge/?version=latest)](https://neural-semigroups.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/inpefess/neural-semigroups/branch/master/graph/badge.svg)](https://codecov.io/gh/inpefess/neural-semigroups)\n\n# Neural Semigroups\n\nHere we try to model Cayley tables of semigroups using neural networks.\n\nThis work was inspired by [a sudoku\nsolver](https://github.com/Kyubyong/sudoku). A solved Sudoku puzzle\nis nothing more than a Cayley table of a quasigroup from 9 items with\nsome well-known additional properties. So, one can imagine a puzzle\nmade from a Cayley table of any other magma, e.g. a semigroup, by\nhiding part of its cells.\n\nThere are two major differences between sudoku and puzzles based on\nsemigroups:\n\n1) it's easy to take a glance on a table to understand whether it is\na sudoku or not. That's why it was possible to encode numbers in a\ntable cells as colour intensities. Sudoku is a picture, and a\nsemigroup is not. It's difficult to check a Cayley table's\nassociativity with a naked eye;\n\n2) Sudoku puzzles are solved by humans for fun and thus catalogued.\nWhen solving a sudoku one knows for sure that there is a unique\nsolution. On the contrary, nobody guesses values in a partially\nfilled Cayley table of a semigroup as a form of amusement. As a\nresult, one can create a puzzle from a full Cayley table of a\nsemigroup but there may be many distinct solutions.\n\n# How to Install\n\nThe best way to install this package is to use `pip`:\n\n```sh\npip install neural-semigroups\n```\n\n# How to use\n\nThe simplest way to get started is to [use Google Colaboratory](https://colab.research.google.com/github/inpefess/neural-semigroups/blob/master/examples/dae_4_colab.ipynb).\n\nTo look at more experimental results for different semigroups cardinalities, you can use [Kaggle](https://kaggle.com):\n\n* [cardinality 4](https://www.kaggle.com/inpefess/neural-semigroups-dae-dim-4)\n* [cardinality 5](https://www.kaggle.com/inpefess/neural-semigroups-dae-dim-5)\n\nThere is also an experimental [notebook](https://github.com/inpefess/neural-semigroups/blob/master/examples/ExperimentNotebook.ipynb) contributed by [Žarko Bulić](https://github.com/zarebulic).\n\n# How to Contribute\n\n[Pull requests](https://github.com/inpefess/neural-semigroups/pulls) are welcome. To start:\n\n```sh\ngit clone https://github.com/inpefess/neural-semigroups\ncd neural-semigroups\n# activate python virtual environment with Python 3.6+\npip install -U pip\npip install -U setuptools wheel poetry\npoetry install\n# recommended but not necessary\npre-commit install\n```\n\nTo check the code quality before creating a pull request, one might run the script [show_report.sh](https://colab.research.google.com/github/inpefess/neural-semigroups/blob/master/show_report.sh). It locally does nearly the same as the CI pipeline after the PR is created.\n\n# Reporting issues or problems with the software\n\nQuestions and bug reports are welcome on [the tracker](https://github.com/inpefess/neural-semigroups/issues). \n\n# More documentation\n\nMore documentation can be found [here](https://neural-semigroups.readthedocs.io/en/latest).\n\n# The paper\n\nThere is also a [paper](https://arxiv.org/abs/2103.07388) with more maths inside. It can be used to [cite](https://dblp.org/rec/journals/corr/abs-2103-07388.html?view=bibtex) the package.\n\nTo reproduce results from the paper, use [this notebook](https://colab.research.google.com/github/inpefess/neural-semigroups/blob/master/examples/train_a_model.ipynb)\n",
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inpefess/neural-semigroups',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)

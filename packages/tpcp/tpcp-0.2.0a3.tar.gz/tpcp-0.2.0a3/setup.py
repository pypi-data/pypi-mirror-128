# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tpcp', 'tpcp._utils', 'tpcp.optimize', 'tpcp.validation']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numpy>=1,<2',
 'pandas>=1,<2',
 'scikit-learn>=1,<2',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'tpcp',
    'version': '0.2.0a3',
    'description': 'Pipeline and Dataset helpers for complex algorithm evaluation.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/tpcp)](https://pypi.org/project/tpcp/)\n[![Documentation Status](https://readthedocs.org/projects/tpcp/badge/?version=latest)](https://tpcp.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/mad-lab-fau/tpcp/branch/main/graph/badge.svg?token=ZNVT5LNYHO)](https://codecov.io/gh/mad-lab-fau/tpcp)\n[![Test and Lint](https://github.com/mad-lab-fau/tpcp/actions/workflows/test-and-lint.yml/badge.svg?branch=main)](https://github.com/mad-lab-fau/tpcp/actions/workflows/test-and-lint.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/tpcp)\n\n# tpcp - Tiny Pipelines for Complex Problems\n\nA generic way to build object-oriented datasets and algorithm pipelines and tools to evaluate them\n\n```\npip install tpcp\n```\n\n## Why?\n\nEvaluating Algorithms - in particular when they contain machine learning - is hard.\nBesides understanding required steps (Cross-validation, Bias, Overfitting, ...), you need to implement the required \nconcepts and make them work together with your algorithms and data.\nIf you are doing something "regular" like training an SVM on tabulary data, amazing libraries like [sklearn](https://scikit-learn.org), \n[tslearn](https://github.com/tslearn-team/tslearn), [pytorch](https://pytorch.org), and many others, have your back.\nBy using their built-in tools (e.g. `sklearn.evaluation.GridSearchCV`) you prevent implementation errors, and you are\nprovided with a sensible structure to organise your code that is well understood in the community.\n\nHowever, often the problems we are trying to solve are not regular.\nThey are **complex**.\nAs an example, here is the summary of the method from one of our [recent papers](https://jneuroengrehab.biomedcentral.com/articles/10.1186/s12984-021-00883-7):\n- We have continues multi-dimensional sensor recordings from multiple participants from a hospital visit and multiple days at home\n- For each participant we have global metadata (age, diagnosis) and daily annotations\n- We want to train Hidden-Markov-Model that can find events in the data streams\n- We need to tune hyper-parameters of the algorithm using a participant-wise cross-validation\n- We want to evaluate the final performance of the algorithm for the settings trained on the hospital data -> tested on home data and trained on home data -> tested on home data\n- Using the same structure we want to evaluate a state-of-the-art algorithm to compare the results\n\nNone of the standard frameworks can easily abstract this problem, because we had none-tabular data, multiple data \nsources per participant, a non-traditional ML algorithm, and a complex train-test split logic.\n\nWith `tpcp` we want to provide a flexible framework to approach such complex problems with structure and confidence.\n\n## How?\n\nTo make `tpcp` easy to use, we try to focus on a couple of key ideas:\n\n- Datasets are Python classes (think `pytorch.datasets`, but more flexible) that can be split, iterated over, and queried\n- Algorithms and Pipelines are Python classes with a simple `run` and `optimize` interface, that can be implemented to fit any problem\n- Everything is a parameter and everything is optimization: In regular ML we differentiate *training* and *hyper-parameter optimization*.\n  In `tpcp` we consider everything that modifies parameters or weights as an *optimization*.\n  This allows to use the same concepts and code interfaces from simple algorithms that just require a gridsearch to optimize a parameter to neuronal network pipelines with hyperparameter Tuning\n- Provide what is difficult, allow to change everything else:\n  `tpcp` implements complicated constructs like cross validation and gridsearch and whenever possible tries to catch obvious errors in your approach.\n  However, for the actual algorithm and dataset you are free to do, whatever is required to solve your current research question.',
    'author': 'Arne Küderle',
    'author_email': 'arne.kuederle@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/tpcp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)

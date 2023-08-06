# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiez',
 'kiez.analysis',
 'kiez.evaluate',
 'kiez.hubness_reduction',
 'kiez.io',
 'kiez.neighbors',
 'kiez.neighbors.approximate',
 'kiez.neighbors.exact',
 'kiez.utils']

package_data = \
{'': ['*']}

install_requires = \
['class-resolver>=0.1.0,<0.2.0',
 'importlib-metadata',
 'joblib>=0.12',
 'numpy>=1.21,<1.22',
 'pandas>=1.3.4,<2.0.0',
 'scikit-learn>=0.24.1',
 'scipy>=1.2',
 'tqdm>=4.56,<4.57']

extras_require = \
{'all': ['ngt>=1.8', 'annoy>=1.17.0,<2.0.0', 'nmslib>=2.1.1,<3.0.0'],
 'annoy': ['annoy>=1.17.0,<2.0.0'],
 'docs': ['Sphinx>=4.3.0,<5.0.0', 'insegel>=1.3.1,<2.0.0'],
 'ngt': ['ngt>=1.8'],
 'nmslib': ['nmslib>=2.1.1,<3.0.0']}

setup_kwargs = {
    'name': 'kiez',
    'version': '0.3.1',
    'description': 'Hubness reduced nearest neighbor search for entity alignment with knowledge graph embeddings',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/kiez/raw/main/docs/kiezlogo.png" alt="kiez logo", width=200/>\n</p>\n\n<h2 align="center"> kiez</h2>\n\n<p align="center">\n<a href="https://github.com/dobraczka/kiez/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/kiez/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href="https://github.com/dobraczka/kiez/actions/workflows/quality.yml"><img alt="Actions Status" src="https://github.com/dobraczka/kiez/actions/workflows/quality.yml/badge.svg?branch=main"></a>\n<a href=\'https://kiez.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/kiez/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n<a href="https://codecov.io/gh/dobraczka/kiez"><img src="https://codecov.io/gh/dobraczka/kiez/branch/main/graph/badge.svg?token=AHBYFKJVLV"/></a>\n<a href="https://pypi.org/project/kiez"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/kiez"></a>\n<a href="https://github.com/dobraczka/kiez/blob/main/LICENSE"><img alt="License BSD3 - Clause" src="https://img.shields.io/badge/license-BSD--3--Clause-blue"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nA Python library for hubness reduced nearest neighbor search for the task of entity alignment with knowledge graph embeddings. The term kiez is a [german word](https://en.wikipedia.org/wiki/Kiez) that refers to a city neighborhood.\n\n## Hubness Reduction\nHubness is a phenomenon that arises in high-dimensional data and describes the fact that a couple of entities are nearest neighbors (NN) of many other entities, while a lot of entities are NN to no one.\nFor entity alignment with knowledge graph embeddings we rely on NN search. Hubness therefore is detrimental to our matching results.\nThis library is intended to make hubness reduction techniques available to data integration projects that rely on (knowledge graph) embeddings in their alignment process. Furthermore kiez incorporates several approximate nearest neighbor (ANN) libraries, to pair the speed advantage of approximate neighbor search with increased accuracy of hubness reduction.\n\n## Installation\nYou can install kiez via pip:\n``` bash\npip install kiez\n```\n\n## Usage\nSimple nearest neighbor search for source entities in target space:\n``` python\nfrom kiez import Kiez\nimport numpy as np\n# create example data\nrng = np.random.RandomState(0)\nsource = rng.rand(100,50)\ntarget = rng.rand(100,50)\n# fit and get neighbors\nk_inst = Kiez()\nk_inst.fit(source, target)\nnn_dist, nn_ind = k_inst.kneighbors()\n```\nUsing ANN libraries and hubness reduction methods:\n``` python\nfrom kiez import Kiez\nimport numpy as np\n# create example data\nrng = np.random.RandomState(0)\nsource = rng.rand(100,50)\ntarget = rng.rand(100,50)\n# prepare algorithm and hubness reduction\nfrom kiez.neighbors import HNSW\nhnsw = HNSW(n_candidates=10)\nfrom kiez.hubness_reduction import CSLS\nhr = CSLS()\n# fit and get neighbors\nk_inst = Kiez(n_neighbors=5, algorithm=hnsw, hubness=hr)\nk_inst.fit(source, target)\nnn_dist, nn_ind = k_inst.kneighbors()\n```\n\n## Documentation\nYou can find more documentation on [readthedocs](https://kiez.readthedocs.io)\n\n## Benchmark\nThe results and configurations of our experiments can be found in a seperate [benchmarking repository](https://github.com/dobraczka/kiez-benchmarking)\n\n## Citation\nIf you find this work useful you can use the following citation:\n```\n@conference{Kiez,\n  author={Daniel Obraczka. and Erhard Rahm.},\n  title={An Evaluation of Hubness Reduction Methods for Entity Alignment with Knowledge Graph Embeddings},\n  booktitle={Proceedings of the 13th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management - KEOD,},\n  year={2021},\n  pages={28-39},\n  publisher={SciTePress},\n  organization={INSTICC},\n  doi={10.5220/0010646400003064},\n  isbn={978-989-758-533-3},\n  issn={2184-3228},\n  url={https://dbs.uni-leipzig.de/file/KIEZ_KEOD_2021_Obraczka_Rahm.pdf},\n}\n```\n\n## Contributing\nPRs and enhancement ideas are always welcome. If you want to build kiez locally use:\n```bash\ngit clone git@github.com:dobraczka/kiez.git\ncd kiez\npoetry install\n```\nTo run the tests (given you are in the kiez folder):\n```bash\npoetry run pytest tests\n```\n## License\n`kiez` is licensed under the terms of the BSD-3-Clause [license](LICENSE.txt).\nSeveral files were modified from [`scikit-hubness`](https://github.com/VarIr/scikit-hubness),\ndistributed under the same [license](external/SCIKIT_HUBNESS_LICENSE.txt).\nThe respective files contain the following tag instead of the full license text.\n\n        SPDX-License-Identifier: BSD-3-Clause\n\nThis enables machine processing of license information based on the SPDX\nLicense Identifiers that are here available: https://spdx.org/licenses/\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dobraczka/kiez',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

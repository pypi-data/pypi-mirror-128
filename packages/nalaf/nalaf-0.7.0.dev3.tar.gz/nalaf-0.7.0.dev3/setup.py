# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nalaf',
 'nalaf.data',
 'nalaf.domain',
 'nalaf.domain.bio',
 'nalaf.features',
 'nalaf.features.relations',
 'nalaf.features.relations.new',
 'nalaf.learning',
 'nalaf.learning.lib',
 'nalaf.preprocessing',
 'nalaf.structures',
 'nalaf.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.5,<5.0',
 'gensim>=0.13.3,<=0.13.4.1',
 'hdfs>=2.5.0,<2.6.0',
 'nltk>=3.0.0,<4.0.0',
 'numpy>=1.16.0,<1.17.0',
 'progress>=1.2,<2.0',
 'python-crfsuite>=0.9.3,<0.10.0',
 'requests>=2.21,<3.0',
 'scikit-learn>=0.18.1,<=0.20.3',
 'scipy>=0.18.1,<1.3',
 'spacy==1.2.0',
 'urllib3>=1.20,<1.25']

setup_kwargs = {
    'name': 'nalaf',
    'version': '0.7.0.dev3',
    'description': 'Natural Language Framework, for NER and RE',
    'long_description': '# ☝️ We moved\n\nThis library is not maintained anymore, and is only ocassionally receiving bugfixes.\n\nWe moved the functionality to train NER & Relation models to [the text annotation tool, tagtog](https://www.tagtog.net):\n\n[![tagtog, The Text Annotation Tool to Train AI](http://docs.tagtog.net/assets/img/circle_2leafstext.png)](https://www.tagtog.net)\n\n---\n---\n---\n\n[![PyPI version](https://badge.fury.io/py/nalaf.svg)](https://badge.fury.io/py/nalaf)\n[![Build Status](https://travis-ci.org/Rostlab/nalaf.svg?branch=develop)](https://travis-ci.org/Rostlab/nalaf)\n[![codecov](https://codecov.io/gh/Rostlab/nalaf/branch/feature%2FExperimental/graph/badge.svg)](https://codecov.io/gh/Rostlab/nalaf)\n\n\n## nalaf - (Na)tural (La)nguage (F)ramework\n\nnalaf is a NLP framework written in python. The goal is to be a general-purpose module-based and easy-to-use framework for common text mining tasks. At the moment two tasks are covered: named-entity recognition (NER) and relationship extraction. These modules support both training and annotating. Associated to these, helper components such as cross-validation training or reading and conversion from different corpora formats are given. At the moment, NER is implemented with Conditional Random Fields (CRFs) and relationship extraction with Support Vector Machines (SVMs) using either linear or tree kernels.\n\nHistorically, the framework started from 2 joint theses at [Rostlab](https://rostlab.org) at [Technische Universität München](http://www.tum.de/en/homepage/) with a focus on bioinformatics / BioNLP. Concretely the first goal was to do extraction of NL mutation mentions. Soon after another master\'s thesis used and generalized the framework to do relationship extraction of transcription factors (TF) interacting with gene or gene products. The nalaf framework is planned to be used in other BioNLP tasks at Rostlab.\n\nAs a result of the original BioNLP focus, some parts of the code are tailored to the biomedical domain. However, current efforts are underway to generalize all parts and this process is almost done. Development is not active and code maintenance is not guaranteed.\n\nCurrent maintainer: [Juan Miguel Cejuela (@juanmirocks)](https://github.com/juanmirocks).\n\n![Pipeline diagram](https://www.lucidchart.com/publicSegments/view/558052b8-fcf0-4e3b-a6b4-05990a008f2c/image.png)\n(_[editable version on Lucidchart of the pipeline diagram](https://www.lucidchart.com/invitations/accept/9236d544-8b56-46c4-9f99-62fdf18e838a); requires log in_)\n\n\n## Install\n\nRequires Python ^3.6\n\n\n### From PyPi\n\n```shell\npip3 install nalaf\npython3 -m nalaf.download_data\n```\n\n### From source\n\n```shell\ngit clone https://github.com/Rostlab/nalaf.git\ncd nalaf\npoetry shell\npoetry update\npython3 -m nalaf.download_data\n```\n\n\n\n\n## Developing\n\n[See wiki](https://github.com/Rostlab/nalaf/wiki/Developer-Info)\n\n\n### Test\n\n```shell\nnosetests\n```\n\n\n### Run Examples\n\nRun `example_annotate.py` for a simple example of annotation with a pre-trained NER model for protein names extraction:\n\n* `python3 example_annotate.py -p 15878741 12625412`\n* `python3 example_annotate.py -s "This is c.A1003G an example"` # see issue https://github.com/Rostlab/nalaf/issues/159\n* `python3 example_annotate.py -d resources/example.txt` # see issue https://github.com/Rostlab/nalaf/issues/159\n',
    'author': 'Juan Miguel Cejuela',
    'author_email': 'juanmi@tagtog.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rostlab/nalaf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<3.7.0',
}


setup(**setup_kwargs)

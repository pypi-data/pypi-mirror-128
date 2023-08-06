# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vak',
 'vak.cli',
 'vak.config',
 'vak.core',
 'vak.core.learncurve',
 'vak.datasets',
 'vak.engine',
 'vak.files',
 'vak.io',
 'vak.metrics',
 'vak.metrics.classification',
 'vak.metrics.distance',
 'vak.models',
 'vak.nn',
 'vak.nn.loss',
 'vak.plot',
 'vak.split',
 'vak.split.algorithms',
 'vak.transforms']

package_data = \
{'': ['*']}

install_requires = \
['SoundFile>=0.10.3',
 'attrs>=19.3.0',
 'crowsetta>=3.1.1',
 'dask[bag]>=2.10.1',
 'evfuncs>=0.3.2',
 'joblib>=0.14.1',
 'matplotlib>=3.3.3',
 'numpy>=1.18.1',
 'pandas>=1.0.1',
 'scipy>=1.4.1',
 'tensorboard>=2.2.0',
 'toml>=0.10.2',
 'torch>=1.4.0,!=1.8.0',
 'torchvision>=0.5.0',
 'tqdm>=4.42.1']

entry_points = \
{'console_scripts': ['vak = vak.__main__:main'],
 'vak.metrics': ['Accuracy = vak.metrics.Accuracy',
                 'Levenshtein = vak.metrics.Levenshtein',
                 'SegmentErrorRate = vak.metrics.SegmentErrorRate'],
 'vak.models': ['TeenyTweetyNetModel = '
                'vak.models.teenytweetynet:TeenyTweetyNetModel']}

setup_kwargs = {
    'name': 'vak',
    'version': '0.4.0b6',
    'description': 'a neural network toolbox for animal vocalizations and bioacoustics',
    'long_description': '[![DOI](https://zenodo.org/badge/173566541.svg)](https://zenodo.org/badge/latestdoi/173566541)\n[![PyPI version](https://badge.fury.io/py/vak.svg)](https://badge.fury.io/py/vak)\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n[![Build Status](https://github.com/NickleDave/vak/actions/workflows/ci.yml/badge.svg)](https://github.com/NickleDave/vak/actions/workflows/ci.yml/badge.svg)\n[![codecov](https://codecov.io/gh/NickleDave/vak/branch/main/graph/badge.svg?token=9Y4XXB2ELA)](https://codecov.io/gh/NickleDave/vak)\n# vak\n## a neural network toolbox for animal vocalizations and bioacoustics\n\n`vak` is a library for researchers studying animal vocalizations--such as \nbirdsong, bat calls, and even human speech--although it may be useful \nto anyone working with bioacoustics data. \nWhile there are many important reasons to study bioacoustics, the scope of `vak` \nis limited to questions related to **vocal learning**, \n"the ability to modify acoustic and syntactic sounds, acquire new sounds via imitation, and produce vocalizations"\n[(Wikipedia)](https://en.wikipedia.org/wiki/Vocal_learning). \nResearch questions related to vocal learning cut across a wide range of fields \nincluding neuroscience, phsyiology, molecular biology, genomics, ecology, and evolution \n[(Wirthlin et al. 2019)](https://www.sciencedirect.com/science/article/pii/S0896627319308396).\n\n`vak` has two main goals:  \n1. make it easier for researchers studying animal vocalizations to \napply neural network algorithms to their data\n2. provide a common framework that will facilitate benchmarking neural \nnetwork algorithms on tasks related to animal vocalizations\n\nCurrently the main use is automated **annotation** of vocalizations and other animal sounds, \nusing artificial neural networks.\nBy **annotation**, we mean something like the example of annotated birdsong shown below:  \n<img src="./doc/images/annotation_example_for_tutorial.png" alt="spectrogram of birdsong with syllables annotated" width="400">\n\nYou give `vak` training data in the form of audio or spectrogram files with annotations, \nand then `vak` helps you train neural network models \nand use the trained models to predict annotations for new files.\n\nWe developed `vak` to benchmark a neural network model we call [`tweetynet`](https://github.com/yardencsGitHub/tweetynet).\nSee pre-print here: [https://www.biorxiv.org/content/10.1101/2020.08.28.272088v2.full.pdf](https://www.biorxiv.org/content/10.1101/2020.08.28.272088v2.full.pdf)  \nWe would love to help you use `vak` to benchmark your own model. \nIf you have questions, please feel free to [raise an issue](https://github.com/NickleDave/vak/issues).\n\n### Installation\nShort version:\n```console\n$ pip install vak\n```\nFor the long version detail, please see:\nhttps://vak.readthedocs.io/en/latest/get_started/installation.html\n\nWe currently test `vak` on Ubuntu and MacOS. We have run on Windows and \nknow of other users successfully running `vak` on that operating system, \nbut installation on Windows will probably require some troubleshooting.\nA good place to start is by searching the [issues](https://github.com/NickleDave/vak/issues).\n\n### Usage\n#### Training models to segment and label vocalizations\nCurrently the easiest way to work with `vak` is through the command line.\n![terminal showing vak help command output](./doc/images/terminalizer/vak-help.gif)\n\nYou run it with `config.toml` files, using one of a handful of commands.\n\nFor more details, please see the "autoannotate" tutorial here:  \nhttps://vak.readthedocs.io/en/latest/tutorial/autoannotate.html\n\n#### Data and folder structures\nTo train models, you provide training data in the form of audio or \nspectrograms files, and annotations for those files.\n\n#### Spectrograms and labels\nThe package can generate spectrograms from `.wav` files or `.cbin` audio files.\nIt can also accept spectrograms in the form of Matlab `.mat` or Numpy `.npz` files.\nThe locations of these files are specified in the `config.toml` file.\n\nThe annotations are parsed by a separate library, `crowsetta`, that \naims to handle common formats like Praat `textgrid` files, and enable \nresearchers to easily work with formats they may have developed in their \nown labs. For more information please see:  \nhttps://crowsetta.readthedocs.io/en/latest/  \nhttps://github.com/NickleDave/crowsetta  \n\n#### Preparing training files\nIt is possible to train on any manually annotated data but there are some useful guidelines:\n* __Use as many examples as possible__ - The results will just be better. Specifically, this code will not label correctly syllables it did not encounter while training and will most probably generalize to the nearest sample or ignore the syllable.\n* __Use noise examples__ - This will make the code very good in ignoring noise.\n* __Examples of syllables on noise are important__ - It is a good practice to start with clean recordings. The code will not perform miracles and is most likely to fail if the audio is too corrupt or masked by noise. Still, training with examples of syllables on the background of cage noises will be beneficial.\n\n### Predicting annotations for audio\nYou can predict annotations for audio files by creating a `config.toml` file with a [PREDICT] section.  \nFor more details, please see the "autoannotate" tutorial here:\nhttps://vak.readthedocs.io/en/latest/tutorial/autoannotate.html\n\n### Support / Contributing\nCurrently we are handling support through the issue tracker on GitHub:  \nhttps://github.com/NickleDave/vak/issues  \nPlease raise an issue there if you run into trouble.  \nThat would be a great place to start if you are interested in contributing, as well.\n\n### Citation\nIf you use vak for a publication, please cite its DOI:  \n[![DOI](https://zenodo.org/badge/173566541.svg)](https://zenodo.org/badge/latestdoi/173566541)\n\n### License\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)  \nis [here](./LICENSE).\n\n### Misc\n#### "Why this name, vak?"\nIt has only three letters, so it is quick to type,\nand it wasn\'t taken on [pypi](https://pypi.org/) yet.\nAlso I guess it has [something to do with speech](https://en.wikipedia.org/wiki/V%C4%81c).\n"vak" rhymes with "squawk" and "talk".\n\n#### Does your library have any poems?\n[Yes.](./doc/poem.md)\n',
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NickleDave/vak',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)

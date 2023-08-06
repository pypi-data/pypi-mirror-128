# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdla']

package_data = \
{'': ['*']}

install_requires = \
['cvxopt>=1.2.0,<2.0.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.19.0,<2.0.0',
 'scikit-learn>=1.0,<2.0',
 'scipy>=1.5,<2.0']

setup_kwargs = {
    'name': 'mdla',
    'version': '1.0.2',
    'description': 'Multivariate Dictionary Learning Algorithm',
    'long_description': '# MDLA - Multivariate Dictionary Learning Algorithm\n\n[![Build Status](https://github.com/sylvchev/mdla/workflows/Test-and-Lint/badge.svg)](https://github.com/sylvchev/mdla/actions?query=branch%3Amaster)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/sylvchev/mdla/branch/master/graph/badge.svg?token=Vba6g9c5pM)](https://codecov.io/gh/sylvchev/mdla)\n\n## Dictionary Learning for the multivariate dataset\n\nThis dictionary learning variant is tailored for dealing with multivariate datasets and\nespecially timeseries, where samples are matrices and the dataset is seen as a tensor.\nDictionary Learning Algorithm (DLA) decompose input vector on a dictionary matrix with a\nsparse coefficient vector, see (a) on figure below. To handle multivariate data, a first\napproach called **multichannel DLA**, see (b) on figure below, is to decompose the matrix\nvector on a dictionary matrix but with sparse coefficient matrices, assuming that a\nmultivariate sample could be seen as a collection of channels explained by the same\ndictionary. Nonetheless, multichannel DLA breaks the "spatial" coherence of multivariate\nsamples, discarding the column-wise relationship existing in the samples. **Multivariate\nDLA**, (c), on figure below, decompose the matrix input on a tensor dictionary, where each\natom is a matrix, with sparse coefficient vectors. In this case, the spatial relationship\nare directly encoded in the dictionary, as each atoms has the same dimension than an input\nsamples.\n\n![dictionaries](https://github.com/sylvchev/mdla/raw/master/img/multidico.png)\n\n(figure from [Chevallier et al., 2014](#biblio) )\n\nTo handle timeseries, two major modifications are brought to DLA:\n\n1. extension to **multivariate** samples\n2. **shift-invariant** approach, The first point is explained above. To implement the\n   second one, there is two possibility, either slicing the input timeseries into small\n   overlapping samples or to have atoms smaller than input samples, leading to a\n   decomposition with sparse coefficients and offsets. In the latter case, the\n   decomposition could be seen as sequence of kernels occuring at different time steps.\n\n![shift invariance](https://github.com/sylvchev/mdla/raw/master/img/audio4spikegram.png)\n\n(figure from [Smith & Lewicki, 2005](#biblio))\n\nThe proposed implementation is an adaptation of the work of the following authors:\n\n- Q. Barthélemy, A. Larue, A. Mayoue, D. Mercier, and J.I. Mars. _Shift & 2D rotation\n  invariant sparse coding for multi- variate signal_. IEEE Trans. Signal Processing,\n  60:1597–1611, 2012.\n- Q. Barthélemy, A. Larue, and J.I. Mars. _Decomposition and dictionary learning for 3D\n  trajectories_. Signal Process., 98:423–437, 2014.\n- Q. Barthélemy, C. Gouy-Pailler, Y. Isaac, A. Souloumiac, A. Larue, and J.I. Mars.\n  _Multivariate temporal dictionary learning for EEG_. Journal of Neuroscience Methods,\n  215:19–28, 2013.\n\n## Dependencies\n\nThe only dependencies are scikit-learn, matplotlib, numpy and scipy.\n\nNo installation is required.\n\n## Example\n\nA straightforward example is:\n\n```python\nimport numpy as np\nfrom mdla import MultivariateDictLearning\nfrom mdla import multivariate_sparse_encode\nfrom numpy.linalg import norm\n\nrng_global = np.random.RandomState(0)\nn_samples, n_features, n_dims = 10, 5, 3\nX = rng_global.randn(n_samples, n_features, n_dims)\n\nn_kernels = 8\ndico = MultivariateDictLearning(n_kernels=n_kernels, max_iter=10).fit(X)\nresidual, code = multivariate_sparse_encode(X, dico)\nprint (\'Objective error for each samples is:\')\nfor i in range(len(residual)):\n    print (\'Sample\', i, \':\', norm(residual[i], \'fro\') + len(code[i]))\n```\n\n## <a id="biblio"></a>Bibliography\n\n- Chevallier, S., Barthelemy, Q., & Atif, J. (2014). [_Subspace metrics for multivariate\n  dictionaries and application to EEG_][1]. In Acoustics, Speech and Signal Processing\n  (ICASSP), IEEE International Conference on (pp. 7178-7182).\n- Smith, E., & Lewicki, M. S. (2005). [_Efficient coding of time-relative structure using\n  spikes_][2]. Neural Computation, 17(1), 19-45\n- Chevallier, S., Barthélemy, Q., & Atif, J. (2014). [_On the need for metrics in\n  dictionary learning assessment_][3]. In European Signal Processing Conference (EUSIPCO),\n  pp. 1427-1431.\n\n[1]: http://dx.doi.org/10.1109/ICASSP.2014.6854993 "Chevallier et al., 2014"\n[2]: http://dl.acm.org/citation.cfm?id=1119614 "Smith and Lewicki, 2005"\n[3]: https://hal-uvsq.archives-ouvertes.fr/hal-01352054/document\n',
    'author': 'Sylvain Chevallier',
    'author_email': 'sylvain.chevallier@uvsq.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sylvchev/mdla',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

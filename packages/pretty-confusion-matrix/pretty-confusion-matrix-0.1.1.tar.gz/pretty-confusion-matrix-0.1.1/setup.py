# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pretty_confusion_matrix']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.5b0,<22.0',
 'flake8>=3.9.2,<4.0.0',
 'isort>=5.8.0,<6.0.0',
 'matplotlib>=3.5.0,<4.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pre-commit>=2.12.1,<3.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'pretty-confusion-matrix',
    'version': '0.1.1',
    'description': 'plot a pretty confusion matrix (like Matlab) in python using seaborn and matplotlib',
    'long_description': "# Confusion Matrix in Python\nPlot a pretty confusion matrix (like Matlab) in python using seaborn and matplotlib\n\n\nCreated on Mon Jun 25 14:17:37 2018\n@author: Wagner Cipriano - wagnerbhbr\n\n\nThis module get a pretty print confusion matrix from a NumPy matrix or from 2 NumPy arrays (`y_test` and `predictions`).\n\n## Installation\n```bash\npip install pretty-confusion-matrix\n```\n\n## Get Started\n\nExamples:\n```python\nimport numpy as np\nimport pandas as pd\nfrom pretty_confusion_matrix import pp_matrix\n\narray = np.array([[13,  0,  1,  0,  2,  0],\n                  [0, 50,  2,  0, 10,  0],\n                  [0, 13, 16,  0,  0,  3],\n                  [0,  0,  0, 13,  1,  0],\n                  [0, 40,  0,  1, 15,  0],\n                  [0,  0,  0,  0,  0, 20]])\n\n# get pandas dataframe\ndf_cm = pd.DataFrame(array, index=range(1, 7), columns=range(1, 7))\n# colormap: see this and choose your more dear\ncmap = 'PuRd'\npp_matrix(df_cm, cmap=cmap)\n```\n![alt text](https://raw.githubusercontent.com/khuyentran1401/pretty-print-confusion-matrix/master/Screenshots/Conf_matrix_default.png)\n\n```python\nimport numpy as np\nfrom pretty_confusion_matrix import pp_matrix_from_data\n\ny_test = np.array([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2,\n                  3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5])\npredic = np.array([1, 2, 4, 3, 5, 1, 2, 4, 3, 5, 1, 2, 3, 4, 4, 1, 4, 3, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 3, 3, 5, 1, 2, 3, 3, 5, 1, 2,\n                  3, 4, 4, 1, 2, 3, 4, 1, 1, 2, 3, 4, 1, 1, 2, 3, 4, 1, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 4, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5])\n\npp_matrix_from_data(y_test, predic)\n```\n\n![alt text](https://raw.githubusercontent.com/khuyentran1401/pretty-print-confusion-matrix/master/Screenshots/Conf_matrix_default_2.png)\n\n\n\n\n## References:\n1. Mat lab confusion matrix\n\n   https://www.mathworks.com/help/nnet/ref/plotconfusion.html\n   \n   https://www.mathworks.com/help/examples/nnet/win64/PlotConfusionMatrixUsingCategoricalLabelsExample_02.png\n\n   https://stackoverflow.com/questions/5821125/how-to-plot-confusion-matrix-with-string-axis-rather-than-integer-in-python/51176855#51176855\n\n\n2. Other Examples in python\n  \n  a) https://stackoverflow.com/a/51176855/1809554\n  \n  b) https://www.programcreek.com/python/example/96197/seaborn.heatmap\n\n  c) http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py\n",
    'author': 'Khuyen Tran',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wcipriano/pretty-print-confusion-matrix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)

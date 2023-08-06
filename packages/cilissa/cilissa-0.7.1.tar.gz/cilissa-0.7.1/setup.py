# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cilissa', 'cilissa.plugins']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0', 'opencv-python>=4.5.2,<5.0.0']

extras_require = \
{'gui': ['PySide6>=6.1.2,<7.0.0']}

entry_points = \
{'console_scripts': ['cilissa = cilissa.__main__:main']}

setup_kwargs = {
    'name': 'cilissa',
    'version': '0.7.1',
    'description': 'Interactive tool for assessing digital image similarity',
    'long_description': '<p align="center">\n    <img src="https://raw.githubusercontent.com/exler/CILISSA/main/docs/_static/logo.png" width="328">\n</p>\n<p align="center">\n    <strong>C</strong>omputer <strong>I</strong>mage <strong>Li</strong>keness A<strong>ss</strong>essing <strong>A</strong>utomation\n</p>\n<p align="center">\n    <!-- Badges -->\n    <img src="https://github.com/exler/CILISSA/actions/workflows/quality.yml/badge.svg">\n    <img src="https://github.com/exler/CILISSA/actions/workflows/tests.yml/badge.svg">\n    <a href="https://codecov.io/gh/exler/CILISSA">\n        <img src="https://codecov.io/gh/exler/CILISSA/branch/main/graph/badge.svg?token=Dixb5buMQr"/>\n    </a>\n    <a href="https://cilissa.readthedocs.io/en/latest/">\n        <img src="https://img.shields.io/readthedocs/cilissa">\n    </a>    \n</p>\n\n## Overview\n\nCILISSA allows for the use of various metrics to perform full-reference image comparisons.\n\nIt features the most popular full-reference image quality metrics, image transformations and translations. \nCILISSA is also very extensible and new operations can be easily added.\n\nCILISSA has an optional Qt-based graphical interface that lets you experiment with various operations, their orders and properties.\n\n## Requirements\n\n* Python >= 3.7\n\n## Installation\n### Install \n```bash\n$ pip install cilissa\n```\n\n### Releases\n\nBinaries for Windows and Linux can be found in [GitHub releases](https://github.com/exler/CILISSA/releases).\n\n## Usage\n\n### GUI\n\nInformation about the GUI can be found in the [cilissa_gui/README.md](cilissa_gui/README.md) file.\n\n### CLI\n\nCurrently the CLI only supports working with a single pair of images.\n\nThe parameters of metrics and transformations can be modified by passing them to the `--kwargs` argument using the following format:\n```\n<operation-name>-<parameter-name>=<value>\n``` \nwhere `parameter-name` uses hyphens (-) instead of underscores (_)\n\n## Documentation\n\nDocumentation is hosted on [Read the Docs](https://cilissa.readthedocs.io/).\n',
    'author': 'Kamil Marut',
    'author_email': 'kamil@kamilmarut.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exler/CILISSA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)

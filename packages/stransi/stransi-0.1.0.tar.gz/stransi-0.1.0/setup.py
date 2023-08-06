# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stransi']

package_data = \
{'': ['*']}

install_requires = \
['ochre>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'stransi',
    'version': '0.1.0',
    'description': 'A lightweight parser for ANSI escape sequences',
    'long_description': '[![Python package](https://github.com/getcuia/stransi/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/stransi/actions/workflows/python-package.yml)\n\n# [stransi](https://github.com/getcuia/stransi#readme) 🖍️\n\n<div align="center">\n    <img class="hero" src="https://github.com/getcuia/stransi/raw/main/banner.jpg" alt="stransi" width="33%" />\n</div>\n\n> I see a `\\033[31m` door, and I want it painted `\\033[30m`.\n\nstransi is a lightweight parser for\n[ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code). It\nimplements a string-like type that is aware of its own ANSI escape sequences,\nand can be used to parse most of the common escape sequences used in terminal\noutput manipulation.\n\n## Features\n\n-   ✨ [Good support of ANSI escape sequences](FEATURES.md)\n-   🎨 Focus on coloring and styling\n-   🛡️ Unsupported `CSI` escape sequences are emitted as tokens\n-   🏜️ Only one dependency: [ochre](https://github.com/getcuia/ochre)\n-   🐍 Python 3.8+\n\n## Credits\n\n[Photo](https://github.com/getcuia/stransi/raw/main/banner.jpg) by\n[Tien Vu Ngoc](https://unsplash.com/@tienvn3012?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)\non\n[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).\n',
    'author': 'Felipe S. S. Schneider',
    'author_email': 'schneider.felipe@posgrad.ufsc.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/getcuia/stransi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

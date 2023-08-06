# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ochre']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ochre',
    'version': '0.1.1',
    'description': 'A tiny Python package for working with colors in a pragmatic way',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/ochre)](https://pypi.org/project/ochre/)\n[![Python package](https://github.com/getcuia/ochre/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/ochre/actions/workflows/python-package.yml)\n[![PyPI - License](https://img.shields.io/pypi/l/ochre)](https://github.com/getcuia/ochre/blob/main/LICENSE)\n\n# [ochre](https://github.com/getcuia/ochre#readme) 🏜️\n\n<div align="center">\n    <img class="hero" src="https://github.com/getcuia/ochre/raw/main/banner.jpg" alt="ochre" width="33%" />\n</div>\n\n> A down-to-earth approach to colors\n\nochre is a tiny Python package for working with colors in a pragmatic way. The\nfocus is on simplicity and ease of use, but also on human perception.\n\n## Features\n\n-   🎨 Focus on [RGB](https://en.wikipedia.org/wiki/RGB_color_model) and\n    [HCL](https://en.wikipedia.org/wiki/HCL_color_space) color spaces\n-   🖥️ [Web color names](https://en.wikipedia.org/wiki/Web_colors#Extended_colors)\n-   ♻️ Color conversions that easily integrate with the\n    [standard `colorsys` module](https://docs.python.org/3/library/colorsys.html)\n-   🗑️ Zero dependencies\n-   🐍 Python 3.8+\n\n## Installation\n\n```console\n$ pip install ochre\n```\n\n## Usage\n\n```python\nIn [1]: from ochre import Hex\n\nIn [2]: color = Hex("#CC7722")\n\nIn [3]: color.web_color\nOut[3]: WebColor(\'peru\')\n\nIn [4]: color = color.hcl\n\nIn [5]: color.hue\nOut[5]: 0.6373041934059377\n\nIn [6]: import math\n\nIn [7]: color.hue += math.radians(30)\n\nIn [8]: color.hue\nOut[8]: 1.1609029690042365\n\nIn [9]: color.web_color\nOut[9]: WebColor(\'goldenrod\')\n```\n\n## Credits\n\n[Photo](https://github.com/getcuia/ochre/raw/main/banner.jpg) by\n[Nicola Carter](https://unsplash.com/@ncarterwilts?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)\non\n[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).\n',
    'author': 'Felipe S. S. Schneider',
    'author_email': 'schneider.felipe@posgrad.ufsc.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/getcuia/ochre',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

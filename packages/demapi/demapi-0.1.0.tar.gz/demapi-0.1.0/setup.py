# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demapi', 'demapi.configure', 'demapi.connector']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'certifi>=2021.10.8,<2022.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'demapi',
    'version': '0.1.0',
    'description': 'Make customizable demotivators and motivators through imgonline.com.ua API. Supports async-await style',
    'long_description': '# DemAPI\n> Make customizable demotivators and motivators through imgonline.com.ua API. Supports async-await style\n\n![Example](./assets/example.png)\n***\n__Documentation__: Check out [GUIDE.md](./GUIDE.md)\n\n[![Coverage Status](https://coveralls.io/repos/github/deknowny/demapi/badge.svg?branch=main)](https://coveralls.io/github/deknowny/demapi?branch=main)\n\n# Features\n* Sync and `async-await` style\n* Customizable titles and explanation (size, colors etc.)\n* Flexible output image (line breaks showed correctly)\n* Not CPU-bound (through unlimited API)\n* Full tests coverage\n* Full typed\n\n## Overview\nConfigure request params such as text, color, size etc.\nAnd then download the image. Optionally save to disk otherwise\nuse `image.content` for raw bytes object\n```python\nimport demapi\n\n\nconf = demapi.Configure(\n    base_photo="example.png",\n    title="The first line",\n    explanation="The second line"\n)\nimage = conf.download()\nimage.save("example.png")\n```\n\nOr via `await` (based on `aiohttp`):\n\n```python\nimage = await conf.coroutine_download()\n```\n\n# Installation\nInstall the latest version through `GitHub`:\n```shell\npython -m pip install https://github.com/deknowny/demapi/archive/main.zip\n```\nOr through `PyPI`\n```shell\npython -m pip install demapi\n```\n\n# Contributing\nCheck out [CONTRIBUTING.md](./CONTRIBUTING.md)\n\n',
    'author': 'Yan Kurbatov',
    'author_email': 'deknowny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deknowny/demapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_static_resources']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0', 'starlette>=0.14.2']

extras_require = \
{':python_version < "3.9"': ['importlib-resources>=5.1.2,<6.0.0']}

setup_kwargs = {
    'name': 'starlette-static-resources',
    'version': '0.1.2',
    'description': '',
    'long_description': "# StaticResources for Starlette\n\nLike [StaticFile](https://www.starlette.io/staticfiles/) but for [package resources](https://docs.python.org/3/library/importlib.html#module-importlib.resources).\n\nExample:\n\n```python\nimport uvicorn\n\nfrom starlette.applications import Starlette\nfrom starlette_static_resources import StaticResources\nfrom importlib_resources import files\n\n\napp = Starlette()\napp.mount('/', StaticResources(resources=files('example.data')), name='static')\n\nuvicorn.run(app, host='0.0.0.0', port=8008)\n```\n\n",
    'author': 'david',
    'author_email': 'davidventura27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidventura/starlette-static-resources',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

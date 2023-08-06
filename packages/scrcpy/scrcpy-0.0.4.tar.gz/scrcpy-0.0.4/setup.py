# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrcpy']

package_data = \
{'': ['*']}

install_requires = \
['adbutils>=0.11.0,<0.12.0', 'av>=8.0.3,<9.0.0', 'numpy>=1.21.4,<2.0.0']

setup_kwargs = {
    'name': 'scrcpy',
    'version': '0.0.4',
    'description': 'A python client for scrcpy, i.e. see & control your android device over adb.',
    'long_description': '# Python Scrcpy Client\n![scrcpy-badge](https://img.shields.io/badge/scrcpy-v1.20-violet)\n\nTODO\n\n## Reference & Appreciation\n- Fork: [py-scrcpy-client](https://github.com/leng-yue/py-scrcpy-client)\n- Core: [scrcpy](https://github.com/Genymobile/scrcpy)\n- Idea: [py-android-viewer](https://github.com/razumeiko/py-android-viewer)\n- CI: [index.py](https://github.com/index-py/index.py)\n',
    'author': 'lengyue',
    'author_email': 'lengyue@lengyue.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/S1M0N38/scrcpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zwave_me_ws']

package_data = \
{'': ['*']}

install_requires = \
['websocket-client>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'zwave-me-ws',
    'version': '0.1.0',
    'description': 'Library, implementing websocket connection to ZWave-Me',
    'long_description': None,
    'author': 'Dmitry Vlasov',
    'author_email': 'kerbalspacema@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lawfulchaos/ZWave-Me-WS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

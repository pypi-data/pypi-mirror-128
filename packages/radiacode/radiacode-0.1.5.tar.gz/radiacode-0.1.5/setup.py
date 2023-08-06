# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radiacode', 'radiacode.decoders', 'radiacode.transports']

package_data = \
{'': ['*']}

install_requires = \
['bluepy>=1.3.0,<2.0.0', 'pyusb>=1.1.1,<2.0.0']

extras_require = \
{'examples': ['aiohttp>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'radiacode',
    'version': '0.1.5',
    'description': 'Library for RadiaCode-101',
    'long_description': "## RadiaCode\n\n[Описание на русском языке](README_ru.md)\n\nThis is a library to work with the radiation detector and spectrometer [RadiaCode-101](https://scan-electronics.com/dosimeters/radiacode/radiacode-101).\n\n***The project is still under development and not stable. Thus, the API might change in the future.***\n\nExample project ([backend](radiacode-examples/webserver.py), [frontend](radiacode-examples/webserver.html)):\n![radiacode-webserver-example](./screenshot.png)\n\n### Installation and example projects\n```\n# install library together with all the dependencies for the examples, remove [examples] if you don't need them\n$ pip3 install 'radiacode[examples]' --upgrade\n\n# launch the webserver from the screenshot above\n# bluetooth: replace with the address of your device\n$ python3 -m radiacode-examples.webserver --bluetooth-mac 52:43:01:02:03:04\n# or the same, but via usb\n$ sudo python3 -m radiacode-examples.webserver\n\n# simple example for outputting information to the terminal, options are similar to the webserver example\n$ python3 -m radiacode-examples.basic\n\n# send data to the public monitoring project narodmon.ru\n$ python3 -m radiacode-examples.narodmon --bluetooth-mac 52:43:01:02:03:04\n```\n\n### Development\n- install [python poetry](https://python-poetry.org/docs/#installation)\n- clone this repository\n- install and run:\n```\n$ poetry install\n$ poetry run python3 radiacode-examples/basic.py --bluetooth-mac 52:43:01:02:03:04 # or without --bluetooth-mac for USB connection\n```\n",
    'author': 'Maxim Andreev',
    'author_email': 'andreevmaxim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cdump/radiacode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)

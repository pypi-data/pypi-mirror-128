# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='hatch-demo',
    version='1rc0',
    long_description='# Hatch Demo\n\n[![PyPI - Version](https://img.shields.io/pypi/v/hatch-demo.svg)](https://pypi.org/project/hatch-demo)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-demo.svg)](https://pypi.org/project/hatch-demo)\n\n-----\n\n**Table of Contents**\n\n- [Installation](#installation)\n- [License](#license)\n\n## Installation\n\n```console\npip install hatch-demo\n```\n\n## License\n\n`hatch-demo` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.\n',
    author_email='"U.N. Owen" <void@some.where>',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=[
        'cowsay',
    ],
    packages=[
        'hatch_demo',
        'tests',
    ],
)

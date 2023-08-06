# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['triotp']

package_data = \
{'': ['*']}

install_requires = \
['Logbook>=1.5.3,<2.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'trio-util>=0.7.0,<0.8.0',
 'trio>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'triotp',
    'version': '0.1.0',
    'description': 'The OTP framework for Python Trio',
    'long_description': "TriOTP, the OTP framework for Python Trio\n=========================================\n\nSee documentation_ for more informations.\n\n.. _documentation: https://linkdd.github.io/triotp\n\n.. image:: https://img.shields.io/pypi/l/triotp.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/triotp/\n   :alt: License\n\n.. image:: https://img.shields.io/pypi/status/triotp.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/triotp/\n   :alt: Development Status\n\n.. image:: https://img.shields.io/pypi/v/triotp.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/triotp/\n   :alt: Latest release\n\n.. image:: https://img.shields.io/pypi/pyversions/triotp.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/triotp/\n   :alt: Supported Python versions\n\n.. image:: https://img.shields.io/pypi/implementation/triotp.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/triotp/\n   :alt: Supported Python implementations\n\n.. image:: https://img.shields.io/pypi/wheel/triotp.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/triotp\n   :alt: Download format\n\n.. image:: https://github.com/linkdd/triotp/actions/workflows/test-suite.yml/badge.svg\n   :target: https://github.com/linkdd/triotp\n   :alt: Build status\n\n.. image:: https://coveralls.io/repos/github/linkdd/triotp/badge.svg?style=flat-square\n   :target: https://coveralls.io/r/linkdd/triotp\n   :alt: Code test coverage\n\n.. image:: https://img.shields.io/pypi/dm/triotp.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/triotp/\n   :alt: Downloads\n\nIntroduction\n------------\n\nThis project is a simplified implementation of the Erlang_/Elixir_ OTP_\nframework.\n\n.. _erlang: https://erlang.org\n.. _elixir: https://elixir-lang.org/\n.. _otp: https://en.wikipedia.org/wiki/Open_Telecom_Platform\n\nIt is built on top of the Trio_ async library and provides:\n\n - **applications:** the root of a supervision tree\n - **supervisors:** automatic restart of children tasks\n - **mailboxes:** message-passing between tasks\n - **gen_servers:** generic server task\n\n.. _trio: https://trio.readthedocs.io\n\nWhy ?\n-----\n\nSince I started writing Erlang/Elixir code, I've always wanted to use its\nconcepts in other languages.\n\nI made this library for fun and most importantly: to see if it was possible.\nAs it turns out, it is!",
    'author': 'David Delassus',
    'author_email': 'david.jose.delassus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linkdd/triotp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

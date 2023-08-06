# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pickledb_ujson']
install_requires = \
['ujson>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'pickledb-ujson',
    'version': '1.0.1',
    'description': 'Fork of PickleDB using ujson',
    'long_description': '<p align="center">\n<i>Software to scrap proxies for my web scrapping and other testing purposes.</i></br></br>\n<a href="https://pypi.org/project/pickledb_ujson/"><img src="https://img.shields.io/pypi/v/pickledb_ujson" alt="PyPI"></a>\n<a href="https://github.com/Divkix/pickledb_ujson/actions"><img src="https://github.com/Divkix/pickledb_ujson/workflows/CI%20%28pip%29/badge.svg" alt="CI (pip)"></a>\n<a href="https://pypi.org/project/pickledb_ujson/"><img src="https://img.shields.io/pypi/pyversions/pickledb_ujson.svg" alt="Supported Python Versions"></a>\n<a href="https://pepy.tech/project/pickledb_ujson"><img src="https://pepy.tech/badge/pickledb_ujson" alt="Downloads"></a>\n</p>\n\n# pickleDB\npickleDB is lightweight, fast, and simple database based on the\n[ujson](https://github.com/ultrajson/ultrajson) module.\nAnd it\'s BSD licensed!\n\n\n## pickleDB is Fun\n```python\n>>> import pickledb_ujson as pickledb\n\n>>> db = pickledb.load(\'test.db\', False)\n\n>>> db.set(\'key\', \'value\')\n\n>>> db.get(\'key\')\n\'value\'\n\n>>> db.dump()\nTrue\n```\n\n## Easy to Install\n```python\n$ pip install pickledb\n```\n\n## Links\n* [website](https://patx.github.io/pickledb)\n* [documentation](https://patx.github.io/pickledb/commands.html)\n* [pypi](http://pypi.python.org/pypi/pickleDB)\n* [github repo](https://github.com/divkix/pickledb_ujson)\n',
    'author': 'Harrison Erd',
    'author_email': 'erdh@mail.broward.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Divkix/pickledb_ujson',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

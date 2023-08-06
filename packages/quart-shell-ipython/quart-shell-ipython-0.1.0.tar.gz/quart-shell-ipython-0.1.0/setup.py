# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['quart_shell_ipython']
install_requires = \
['ipython', 'quart']

setup_kwargs = {
    'name': 'quart-shell-ipython',
    'version': '0.1.0',
    'description': 'Startup the quart shell with ipython',
    'long_description': '# quart-shell-ipython\n\ngenerated from flask-shell-ipython\n\nStart quart shell with ipython, if it installed\n',
    'author': 'hs',
    'author_email': 'huangxiaohen2738@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ponytailer/quart-shell-ipython.git',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

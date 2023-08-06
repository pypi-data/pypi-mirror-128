# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['vectorx']
setup_kwargs = {
    'name': 'vectorx',
    'version': '1.0.0',
    'description': 'class Vector(x=0, y=0, z=0)',
    'long_description': None,
    'author': 'semenchuk Community',
    'author_email': 'hootuk@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

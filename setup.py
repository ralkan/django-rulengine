#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

VERSION = (0, 0, 3)
__version__ = '.'.join(map(str, VERSION))

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

packages = find_packages()

setup(
    name='django-rulengine',
    version=__version__,
    description='A simple rule engine for django admin',
    long_description=README,
    url='https://github.com/ralkan/django-rulengine',
    download_url='https://github.com/ralkan/django-rulengine/tarball/%s' % (
        __version__,),
    author='Resul Alkan',
    author_email='me@resulalkan.com',
    license='MIT',
    keywords='django,rule engine,django admin,admin rule engine',
    packages=packages,
    install_requires=[
        'Django==1.7.10',
        'django-nested-inline==0.3.7',
        'rulengine==0.0.6'
    ]
)

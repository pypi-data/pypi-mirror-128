#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import sys
import re
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

with open('xfactor/__init__.py') as fd:
    __version__ = re.search("__version__ = '(.*)'", fd.read()).group(1)

setup(
    name='xfactor',
    version=__version__,
    url='https://github.com/yhtang',
    license='All rights reserved',
    author='Yu-Hang Tang',
    install_requires=[
        'ipython',
        'matplotlib',
        'sympy'
    ],
    extras_require={},
    # cmdclass={'test': Tox},
    author_email='Tang.Maxin@gmail.com',
    description='Matplotlib magic header for easy switch between pgf and svg backends',
    long_description="",
    long_description_content_type="text/markdown",
    packages=find_packages(exclude='test'),
    package_data={
        '': ['*.txt', '*.ttf', '*.otf'],
    },
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
    ]
)

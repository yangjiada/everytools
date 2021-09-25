#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

DIR = path.dirname(path.abspath(__file__))
INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()

with open(path.join(DIR, 'README.md'), encoding='utf-8') as f:
    README = f.read()

setup(
    name='everytools',
    packages=['everytools'],
    description="python tools for everything",
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_PACKAGES,
    version='0.0.1.0',
    url='https://github.com/yangjiada/everything',
    author='Jan Yang',
    author_email='yang.jiada@foxmail.com',
    keywords=['everything', 'everytools', 'windows', 'file', 'search', 'file search'],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-sugar'
    ],
    package_data={
        '': ['dll/*.dll'],
    },
    python_requires='>=3.6'
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

DIR = path.dirname(path.abspath(__file__))
INSTALL_PACKAGES = open(path.join(DIR, "requirements.txt")).read().splitlines()

with open(path.join(DIR, "README.md"), encoding="utf-8") as f:
    README = f.read()

setup(
    name="everytools",
    packages=find_packages(),  # 自动查找所有子包
    description="Python tools for Everything search engine",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_PACKAGES,
    version="0.0.2.0",  # 更新版本号
    url="https://github.com/yangjiada/everytools",
    author="Jan Yang",
    author_email="yang.jiada@foxmail.com",
    keywords=[
        "everything",
        "everytools",
        "windows",
        "file",
        "search",
        "file search",
        "everything sdk",
    ],
    tests_require=["pytest", "pytest-cov", "pytest-sugar"],
    package_data={
        "": ["dll/*.dll"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)

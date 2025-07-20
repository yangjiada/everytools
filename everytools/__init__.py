#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
everytools - Python调用everything进行文件搜索的工具，只适用于Windows系统。
Python wrapper for Everything search tool, for Windows only.
"""

__version__ = "0.2.2"
__author__ = "Jan Yang"
__email__ = "yang.jiada@foxmail.com"

# 向后兼容的类
from .everytools import EveryTools

# 新API
from .query.search import Search, SearchBuilder
from .query.filters import (
    FileFilter,
    FolderFilter,
    DateFilter,
    MediaFilter,
    DocumentFilter,
)
from .constants import SortType, RequestFlag, ErrorCode

__all__ = [
    "EveryTools",  # 向后兼容
    "Search",
    "SearchBuilder",
    "FileFilter",
    "FolderFilter",
    "DateFilter",
    "MediaFilter",
    "DocumentFilter",
    "SortType",
    "RequestFlag",
    "ErrorCode",
]

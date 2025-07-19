#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
核心包
Core package for Everything SDK
"""

from .dll_loader import get_dll_loader
from .result import ResultSet, FileResult
from .api_wrapper import get_api, EverythingAPI

__all__ = ["get_dll_loader", "ResultSet", "FileResult", "get_api", "EverythingAPI"]

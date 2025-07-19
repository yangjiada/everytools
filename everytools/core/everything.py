#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..everytools import EveryTools


class Everything:
    """封装EveryTools类的现代接口"""

    def __init__(self, machine=64):
        self._et = EveryTools(machine)
        self._query = ""
        self._match_case = False
        self._match_path = False
        self._match_whole_word = False
        self._regex = False
        self._max_results = None
        self._sort_type = 1  # 默认按名称升序

    def search(self, query):
        """设置搜索关键词"""
        self._query = query
        return self

    def match_case(self, enabled=True):
        """设置是否区分大小写"""
        self._match_case = enabled
        return self

    def match_path(self, enabled=True):
        """设置是否匹配路径"""
        self._match_path = enabled
        return self

    def match_whole_word(self, enabled=True):
        """设置是否全字匹配"""
        self._match_whole_word = enabled
        return self

    def use_regex(self, enabled=True):
        """设置是否使用正则表达式"""
        self._regex = enabled
        return self

    def sort_by(self, sort_type):
        """设置结果排序方式"""
        self._sort_type = sort_type
        return self

    def limit(self, max_results):
        """限制返回结果数量"""
        self._max_results = max_results
        return self

    def results(self):
        """执行搜索并返回结果"""
        self._et.search(
            self._query,
            math_path=self._match_path,
            math_case=self._match_case,
            whole_world=self._match_whole_word,
            regex=self._regex,
        )

        return self._et.results(max_num=self._max_results, sort_type=self._sort_type)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # 不需要额外清理

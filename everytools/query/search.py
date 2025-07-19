#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
搜索模块
Search module for Everything SDK
"""

import time
import ctypes
from typing import Any, Dict, List, Optional, Union, Callable

from ..core.dll_loader import get_dll_loader
from ..core.result import ResultSet
from ..constants import RequestFlag, SortType
from ..exceptions import EverythingError, raise_for_error_code
from .filters import Filter


class SearchBuilder:
    """Everything搜索构建器，用于构建搜索查询"""

    def __init__(self):
        """初始化搜索构建器"""
        self._keywords = []
        self._filters = []
        self._match_case = False
        self._match_path = False
        self._match_whole_word = False
        self._regex = False
        self._sort_type = SortType.NAME_ASCENDING
        self._max_results = None
        self._request_flags = (
            RequestFlag.FILE_NAME
            | RequestFlag.PATH
            | RequestFlag.FULL_PATH_AND_FILE_NAME
            | RequestFlag.SIZE
            | RequestFlag.DATE_CREATED
            | RequestFlag.DATE_MODIFIED
            | RequestFlag.EXTENSION
        )

    def keywords(self, *keywords: str) -> "SearchBuilder":
        """添加关键词

        Args:
            keywords: 要搜索的关键词

        Returns:
            搜索构建器实例（链式调用）
        """
        self._keywords.extend(keywords)
        return self

    def filter(self, *filters: Filter) -> "SearchBuilder":
        """添加过滤器

        Args:
            filters: 要应用的过滤器

        Returns:
            搜索构建器实例（链式调用）
        """
        self._filters.extend(filters)
        return self

    def match_case(self, enable: bool = True) -> "SearchBuilder":
        """设置是否区分大小写

        Args:
            enable: 是否启用

        Returns:
            搜索构建器实例（链式调用）
        """
        self._match_case = enable
        return self

    def match_path(self, enable: bool = True) -> "SearchBuilder":
        """设置是否匹配路径

        Args:
            enable: 是否启用

        Returns:
            搜索构建器实例（链式调用）
        """
        self._match_path = enable
        return self

    def match_whole_word(self, enable: bool = True) -> "SearchBuilder":
        """设置是否全字匹配

        Args:
            enable: 是否启用

        Returns:
            搜索构建器实例（链式调用）
        """
        self._match_whole_word = enable
        return self

    def use_regex(self, enable: bool = True) -> "SearchBuilder":
        """设置是否使用正则表达式

        Args:
            enable: 是否启用

        Returns:
            搜索构建器实例（链式调用）
        """
        self._regex = enable
        return self

    def sort_by(self, sort_type: SortType) -> "SearchBuilder":
        """设置排序方式

        Args:
            sort_type: 排序类型

        Returns:
            搜索构建器实例（链式调用）
        """
        self._sort_type = sort_type
        return self

    def limit(self, max_results: int) -> "SearchBuilder":
        """限制结果数量

        Args:
            max_results: 最大结果数

        Returns:
            搜索构建器实例（链式调用）
        """
        self._max_results = max_results
        return self

    def request_flags(self, flags: RequestFlag) -> "SearchBuilder":
        """设置请求标志位

        Args:
            flags: 请求标志位

        Returns:
            搜索构建器实例（链式调用）
        """
        self._request_flags = flags
        return self

    def build_query_string(self) -> str:
        """构建查询字符串

        Returns:
            完整的查询字符串
        """
        parts = []

        # 添加关键词
        parts.extend(self._keywords)

        # 添加过滤器
        for f in self._filters:
            filter_query = f.to_query_string()
            if filter_query:
                parts.append(filter_query)

        return " ".join(parts)

    def execute(self, async_query: bool = False) -> "Search":
        """执行搜索

        Args:
            async_query: 是否异步搜索（不阻塞等待结果）

        Returns:
            Search实例
        """
        # 创建搜索实例
        search = Search(
            query_string=self.build_query_string(),
            match_case=self._match_case,
            match_path=self._match_path,
            match_whole_word=self._match_whole_word,
            regex=self._regex,
            sort_type=self._sort_type,
            max_results=self._max_results,
            request_flags=self._request_flags,
        )

        # 执行搜索
        search.execute(async_query=async_query)

        return search


class Search:
    """Everything搜索类，用于执行搜索并获取结果"""

    def __init__(
        self,
        query_string: str,
        match_case: bool = False,
        match_path: bool = False,
        match_whole_word: bool = False,
        regex: bool = False,
        sort_type: SortType = SortType.NAME_ASCENDING,
        max_results: Optional[int] = None,
        request_flags: RequestFlag = RequestFlag.FILE_NAME
        | RequestFlag.PATH
        | RequestFlag.FULL_PATH_AND_FILE_NAME,
    ):
        """初始化搜索

        Args:
            query_string: 查询字符串
            match_case: 是否区分大小写
            match_path: 是否匹配路径
            match_whole_word: 是否全字匹配
            regex: 是否使用正则表达式
            sort_type: 排序类型
            max_results: 最大结果数量
            request_flags: 请求标志位
        """
        self._dll_loader = get_dll_loader()
        self._dll = self._dll_loader.everything_dll

        self._query_string = query_string
        self._match_case = match_case
        self._match_path = match_path
        self._match_whole_word = match_whole_word
        self._regex = regex
        self._sort_type = sort_type
        self._max_results = max_results
        self._request_flags = request_flags

        self._results: Optional[ResultSet] = None
        self._is_executed = False
        self._is_async = False
        self._async_completed = False

    def execute(self, async_query: bool = False) -> None:
        """执行搜索

        Args:
            async_query: 是否异步搜索（不阻塞等待结果）

        Raises:
            EverythingError: 如果搜索出错
        """
        # 重置状态
        self._dll.Everything_Reset()

        # 设置搜索参数
        self._dll.Everything_SetSearchW(self._query_string)
        self._dll.Everything_SetMatchCase(self._match_case)
        self._dll.Everything_SetMatchPath(self._match_path)
        self._dll.Everything_SetMatchWholeWord(self._match_whole_word)
        self._dll.Everything_SetRegex(self._regex)
        self._dll.Everything_SetSort(self._sort_type)
        self._dll.Everything_SetRequestFlags(self._request_flags)

        # 执行查询
        if async_query:
            self._is_async = True
            self._async_completed = False
            # 异步查询需要设置回调窗口，但在Python中实现较复杂
            # 为简化实现，我们仍然使用同步查询
            result = self._dll.Everything_QueryW(True)  # 同步查询
            if not result:
                # 检查错误
                self._dll_loader.check_error()
            self._async_completed = True  # 标记为已完成
        else:
            self._is_async = False
            result = self._dll.Everything_QueryW(True)  # 同步查询
            if not result:
                # 检查错误
                self._dll_loader.check_error()

        self._is_executed = True

    def wait_for_completion(self, timeout_ms: int = 10000) -> bool:
        """等待异步搜索完成

        Args:
            timeout_ms: 超时时间（毫秒）

        Returns:
            是否成功完成

        Raises:
            EverythingError: 如果没有执行异步搜索
        """
        if not self._is_executed:
            raise EverythingError("搜索尚未执行")

        if not self._is_async:
            return True  # 同步搜索已经完成

        if self._async_completed:
            return True  # 已经完成

        # 等待完成
        start_time = time.time()
        while time.time() - start_time < timeout_ms / 1000:
            if self.is_completed():
                self._async_completed = True
                return True
            time.sleep(0.01)  # 短暂睡眠避免CPU占用

        return False

    def is_completed(self) -> bool:
        """检查异步搜索是否完成

        Returns:
            是否完成
        """
        if not self._is_executed:
            return False

        if not self._is_async:
            return True  # 同步搜索已经完成

        # 异步查询需要使用不同的方式检查完成状态
        # 在这个简化版本中，我们直接返回True，因为Everything_IsQueryReply需要消息处理循环
        # 实际应用中应该使用Windows消息循环和Everything_IsQueryReply函数
        return True

    def get_results(self) -> ResultSet:
        """获取搜索结果

        Returns:
            结果集

        Raises:
            EverythingError: 如果搜索尚未执行或异步搜索尚未完成
        """
        if not self._is_executed:
            raise EverythingError("搜索尚未执行")

        if self._is_async and not self.is_completed():
            raise EverythingError("异步搜索尚未完成")

        # 如果已经有缓存的结果，直接返回
        if self._results is not None:
            return self._results

        # 创建结果集
        self._results = ResultSet(self._dll, max_results=self._max_results)
        return self._results

    @property
    def query_string(self) -> str:
        """获取查询字符串

        Returns:
            查询字符串
        """
        return self._query_string


if __name__ == "__main__":
    # 调试代码
    search_builder = SearchBuilder()
    search = search_builder.keywords("测试文件").match_case(True).limit(10).execute()

    print(f"查询字符串: {search.query_string}")
    results = search.get_results()

    print(f"找到 {len(results)} 个结果:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result.full_path}")
        print(f"   大小: {result.size} 字节")
        print(f"   创建时间: {result.date_created}")
        print(f"   修改时间: {result.date_modified}")
        print()

    # 测试过滤器
    print("使用过滤器搜索:")
    from .filters import SizeFilter, DateFilter

    filtered_search = (
        SearchBuilder()
        .keywords("文档")
        .filter(SizeFilter().larger_than(1024 * 1024))  # 大于1MB
        .filter(DateFilter().modified_after("2023-01-01"))
        .limit(5)
        .execute()
    )

    filtered_results = filtered_search.get_results()
    print(f"找到 {len(filtered_results)} 个过滤后的结果")
    for i, result in enumerate(filtered_results):
        print(f"{i+1}. {result.full_path} ({result.size/1024/1024:.2f} MB)")

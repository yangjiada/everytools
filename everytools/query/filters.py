#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
搜索过滤器模块
Search filters module for Everything SDK
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Set, Union


class Filter(ABC):
    """过滤器基类"""

    @abstractmethod
    def to_query_string(self) -> str:
        """转换为Everything搜索查询字符串

        Returns:
            查询字符串
        """
        pass


class FileFilter(Filter):
    """文件过滤器"""

    def __init__(self):
        """初始化文件过滤器"""
        self._extensions: Set[str] = set()
        self._min_size: Optional[int] = None
        self._max_size: Optional[int] = None
        self._content: Optional[str] = None
        self._duplicates: bool = False

    def with_extensions(self, *extensions: str) -> "FileFilter":
        """按文件扩展名过滤

        Args:
            extensions: 文件扩展名列表，不需要包含点

        Returns:
            过滤器实例（链式调用）
        """
        for ext in extensions:
            ext = ext.lstrip(".")  # 移除前导点，确保格式一致
            self._extensions.add(ext)
        return self

    def with_size_range(
        self, min_size: Optional[int] = None, max_size: Optional[int] = None
    ) -> "FileFilter":
        """按文件大小范围过滤

        Args:
            min_size: 最小文件大小（字节）
            max_size: 最大文件大小（字节）

        Returns:
            过滤器实例（链式调用）
        """
        self._min_size = min_size
        self._max_size = max_size
        return self

    def with_content(self, content: str) -> "FileFilter":
        """按文件内容过滤（仅文本文件）

        Args:
            content: 要搜索的内容

        Returns:
            过滤器实例（链式调用）
        """
        self._content = content
        return self

    def duplicates_only(self, enable: bool = True) -> "FileFilter":
        """仅显示重复文件

        Args:
            enable: 是否启用

        Returns:
            过滤器实例（链式调用）
        """
        self._duplicates = enable
        return self

    def to_query_string(self) -> str:
        """转换为Everything搜索查询字符串

        Returns:
            查询字符串
        """
        parts = []

        # 添加文件类型过滤
        if self._extensions:
            exts = ";".join(self._extensions)
            parts.append(f"ext:{exts}")

        # 添加大小过滤
        if self._min_size is not None or self._max_size is not None:
            if self._min_size is not None and self._max_size is not None:
                parts.append(f"size:{self._min_size}..{self._max_size}")
            elif self._min_size is not None:
                parts.append(f"size:>{self._min_size}")
            else:
                parts.append(f"size:<{self._max_size}")

        # 添加内容过滤
        if self._content:
            # 使用引号包裹内容，确保空格不会被视为分隔符
            content = self._content.replace('"', '\\"')  # 转义引号
            parts.append(f'content:"{content}"')

        # 添加重复文件过滤
        if self._duplicates:
            parts.append("dupe:")

        return " ".join(parts)


class FolderFilter(Filter):
    """文件夹过滤器"""

    def __init__(self):
        """初始化文件夹过滤器"""
        self._empty: Optional[bool] = None
        self._min_items: Optional[int] = None
        self._max_items: Optional[int] = None

    def empty_only(self, enable: bool = True) -> "FolderFilter":
        """仅显示空文件夹

        Args:
            enable: 是否启用

        Returns:
            过滤器实例（链式调用）
        """
        self._empty = enable
        return self

    def with_items_count(
        self, min_items: Optional[int] = None, max_items: Optional[int] = None
    ) -> "FolderFilter":
        """按文件夹中的项目数量过滤

        Args:
            min_items: 最小项目数
            max_items: 最大项目数

        Returns:
            过滤器实例（链式调用）
        """
        self._min_items = min_items
        self._max_items = max_items
        return self

    def to_query_string(self) -> str:
        """转换为Everything搜索查询字符串

        Returns:
            查询字符串
        """
        parts = ["folder:"]

        # 添加空文件夹过滤
        if self._empty:
            parts.append("empty:")

        # 添加项目数量过滤
        if self._min_items is not None or self._max_items is not None:
            if self._min_items is not None and self._max_items is not None:
                parts.append(f"count:{self._min_items}..{self._max_items}")
            elif self._min_items is not None:
                parts.append(f"count:>{self._min_items}")
            else:
                parts.append(f"count:<{self._max_items}")

        return " ".join(parts)


class DateFilter(Filter):
    """日期过滤器"""

    def __init__(self):
        """初始化日期过滤器"""
        self._type: str = "modified"  # 默认为修改日期
        self._start_date: Optional[str] = None
        self._end_date: Optional[str] = None

    def by_created_date(self) -> "DateFilter":
        """按创建日期过滤

        Returns:
            过滤器实例（链式调用）
        """
        self._type = "created"
        return self

    def by_modified_date(self) -> "DateFilter":
        """按修改日期过滤

        Returns:
            过滤器实例（链式调用）
        """
        self._type = "modified"
        return self

    def by_accessed_date(self) -> "DateFilter":
        """按访问日期过滤

        Returns:
            过滤器实例（链式调用）
        """
        self._type = "accessed"
        return self

    def in_range(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> "DateFilter":
        """设置日期范围

        Args:
            start_date: 开始日期，格式为YYYY-MM-DD
            end_date: 结束日期，格式为YYYY-MM-DD

        Returns:
            过滤器实例（链式调用）
        """
        self._start_date = start_date
        self._end_date = end_date
        return self

    def after(self, date: str) -> "DateFilter":
        """设置日期在指定日期之后

        Args:
            date: 日期，格式为YYYY-MM-DD

        Returns:
            过滤器实例（链式调用）
        """
        self._start_date = date
        return self

    def before(self, date: str) -> "DateFilter":
        """设置日期在指定日期之前

        Args:
            date: 日期，格式为YYYY-MM-DD

        Returns:
            过滤器实例（链式调用）
        """
        self._end_date = date
        return self

    def modified_after(self, date: str) -> "DateFilter":
        """设置修改日期在指定日期之后（便捷方法）

        Args:
            date: 日期，格式为YYYY-MM-DD

        Returns:
            过滤器实例（链式调用）
        """
        return self.by_modified_date().after(date)

    def created_after(self, date: str) -> "DateFilter":
        """设置创建日期在指定日期之后（便捷方法）

        Args:
            date: 日期，格式为YYYY-MM-DD

        Returns:
            过滤器实例（链式调用）
        """
        return self.by_created_date().after(date)

    @classmethod
    def today(cls) -> "DateFilter":
        """创建今天的日期过滤器

        Returns:
            过滤器实例
        """
        filter_obj = cls()
        filter_obj._start_date = "today"
        return filter_obj

    @classmethod
    def yesterday(cls) -> "DateFilter":
        """创建昨天的日期过滤器

        Returns:
            过滤器实例
        """
        filter_obj = cls()
        filter_obj._start_date = "yesterday"
        return filter_obj

    @classmethod
    def this_week(cls) -> "DateFilter":
        """创建本周的日期过滤器

        Returns:
            过滤器实例
        """
        filter_obj = cls()
        filter_obj._start_date = "thisweek"
        return filter_obj

    @classmethod
    def last_week(cls) -> "DateFilter":
        """创建上周的日期过滤器

        Returns:
            过滤器实例
        """
        filter_obj = cls()
        filter_obj._start_date = "lastweek"
        return filter_obj

    def to_query_string(self) -> str:
        """转换为Everything搜索查询字符串

        Returns:
            查询字符串
        """
        # 处理特殊的日期关键词
        special_dates = ["today", "yesterday", "thisweek", "lastweek"]

        if self._start_date in special_dates:
            return self._start_date

        # 根据日期类型选择前缀
        prefix_map = {"created": "dc", "modified": "dm", "accessed": "da"}
        prefix = prefix_map.get(self._type, "dm")

        if self._start_date is not None and self._end_date is not None:
            return f"{prefix}:{self._start_date}..{self._end_date}"
        elif self._start_date is not None:
            return f"{prefix}:>{self._start_date}"
        elif self._end_date is not None:
            return f"{prefix}:<{self._end_date}"
        else:
            return ""


class MediaFilter(FileFilter):
    """媒体文件过滤器"""

    def __init__(self, media_type: str = "all"):
        """初始化媒体文件过滤器

        Args:
            media_type: 媒体类型，可以是'audio', 'video', 'image'或'all'
        """
        super().__init__()
        self._media_type = media_type

        # 添加默认扩展名
        if media_type == "audio" or media_type == "all":
            self.with_extensions(
                "mp3",
                "wav",
                "flac",
                "aac",
                "ogg",
                "wma",
                "m4a",
                "aiff",
                "alac",
                "ape",
                "midi",
                "mid",
            )

        if media_type == "video" or media_type == "all":
            self.with_extensions(
                "mp4",
                "avi",
                "mkv",
                "mov",
                "wmv",
                "flv",
                "webm",
                "m4v",
                "mpg",
                "mpeg",
                "3gp",
                "ts",
            )

        if media_type == "image" or media_type == "all":
            self.with_extensions(
                "jpg",
                "jpeg",
                "png",
                "gif",
                "bmp",
                "tiff",
                "webp",
                "raw",
                "svg",
                "psd",
                "ai",
                "ico",
            )


class SizeFilter(Filter):
    """文件大小过滤器"""

    def __init__(self):
        """初始化大小过滤器"""
        self._min_size: Optional[int] = None
        self._max_size: Optional[int] = None

    def larger_than(self, size: int) -> "SizeFilter":
        """设置文件大小大于指定值

        Args:
            size: 文件大小（字节）

        Returns:
            过滤器实例（链式调用）
        """
        self._min_size = size
        return self

    def smaller_than(self, size: int) -> "SizeFilter":
        """设置文件大小小于指定值

        Args:
            size: 文件大小（字节）

        Returns:
            过滤器实例（链式调用）
        """
        self._max_size = size
        return self

    def between(self, min_size: int, max_size: int) -> "SizeFilter":
        """设置文件大小在指定范围内

        Args:
            min_size: 最小文件大小（字节）
            max_size: 最大文件大小（字节）

        Returns:
            过滤器实例（链式调用）
        """
        self._min_size = min_size
        self._max_size = max_size
        return self

    def larger_than_mb(self, size_mb: float) -> "SizeFilter":
        """设置文件大小大于指定MB值（便捷方法）

        Args:
            size_mb: 文件大小（MB）

        Returns:
            过滤器实例（链式调用）
        """
        return self.larger_than(int(size_mb * 1024 * 1024))

    def smaller_than_mb(self, size_mb: float) -> "SizeFilter":
        """设置文件大小小于指定MB值（便捷方法）

        Args:
            size_mb: 文件大小（MB）

        Returns:
            过滤器实例（链式调用）
        """
        return self.smaller_than(int(size_mb * 1024 * 1024))

    def larger_than_gb(self, size_gb: float) -> "SizeFilter":
        """设置文件大小大于指定GB值（便捷方法）

        Args:
            size_gb: 文件大小（GB）

        Returns:
            过滤器实例（链式调用）
        """
        return self.larger_than(int(size_gb * 1024 * 1024 * 1024))

    def to_query_string(self) -> str:
        """转换为Everything搜索查询字符串

        Returns:
            查询字符串
        """
        if self._min_size is not None and self._max_size is not None:
            return f"size:{self._min_size}..{self._max_size}"
        elif self._min_size is not None:
            return f"size:>{self._min_size}"
        elif self._max_size is not None:
            return f"size:<{self._max_size}"
        else:
            return ""


class DocumentFilter(FileFilter):
    """文档文件过滤器"""

    def __init__(self, doc_type: str = "all"):
        """初始化文档文件过滤器

        Args:
            doc_type: 文档类型，可以是'office', 'pdf', 'text'或'all'
        """
        super().__init__()
        self._doc_type = doc_type

        # 添加默认扩展名
        if doc_type == "office" or doc_type == "all":
            self.with_extensions(
                "doc",
                "docx",
                "xls",
                "xlsx",
                "ppt",
                "pptx",
                "odt",
                "ods",
                "odp",
                "rtf",
                "dotx",
            )

        if doc_type == "pdf" or doc_type == "all":
            self.with_extensions("pdf")

        if doc_type == "text" or doc_type == "all":
            self.with_extensions(
                "txt",
                "md",
                "json",
                "xml",
                "html",
                "htm",
                "csv",
                "log",
                "ini",
                "cfg",
                "conf",
            )

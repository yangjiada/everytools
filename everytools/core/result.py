#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
搜索结果处理模块
Search result module
"""

import os
import ctypes
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional, Union
import struct
import time

from ..utils.time_utils import filetime_to_datetime, filetime_to_str, DEBUG


class FileResult:
    """单个文件或文件夹的搜索结果"""

    def __init__(
        self,
        name: str,
        path: str,
        full_path: Optional[str] = None,
        size: Optional[int] = None,
        date_created: Optional[Union[datetime, str]] = None,
        date_modified: Optional[Union[datetime, str]] = None,
        date_accessed: Optional[Union[datetime, str]] = None,
        date_run: Optional[Union[datetime, str]] = None,
        extension: Optional[str] = None,
        attributes: Optional[int] = None,
        is_file: bool = True,
        is_folder: bool = False,
        is_volume: bool = False,
        run_count: Optional[int] = None,
        highlighted_name: Optional[str] = None,
        highlighted_path: Optional[str] = None,
    ):
        """初始化文件结果

        Args:
            name: 文件名
            path: 文件路径
            full_path: 完整路径（包含文件名）
            size: 文件大小（字节）
            date_created: 创建日期
            date_modified: 修改日期
            date_accessed: 访问日期
            date_run: 运行日期
            extension: 文件扩展名
            attributes: 文件属性
            is_file: 是否为文件
            is_folder: 是否为文件夹
            is_volume: 是否为卷
            run_count: 运行次数
            highlighted_name: 高亮显示的文件名
            highlighted_path: 高亮显示的路径
        """
        self.name = name
        self.path = path
        self.full_path = full_path or (
            os.path.join(path, name) if path and name else None
        )
        self.size = size
        self.date_created = date_created
        self.date_modified = date_modified
        self.date_accessed = date_accessed
        self.date_run = date_run
        self.extension = extension
        self.attributes = attributes
        self.is_file = is_file
        self.is_folder = is_folder
        self.is_volume = is_volume
        self.run_count = run_count
        self.highlighted_name = highlighted_name
        self.highlighted_path = highlighted_path

    def to_dict(self) -> Dict[str, Any]:
        """将结果转换为字典

        Returns:
            包含所有属性的字典
        """
        return {
            "name": self.name,
            "path": self.path,
            "full_path": self.full_path,
            "size": self.size,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "date_accessed": self.date_accessed,
            "date_run": self.date_run,
            "extension": self.extension,
            "attributes": self.attributes,
            "is_file": self.is_file,
            "is_folder": self.is_folder,
            "is_volume": self.is_volume,
            "run_count": self.run_count,
            "highlighted_name": self.highlighted_name,
            "highlighted_path": self.highlighted_path,
        }

    def __str__(self) -> str:
        """字符串表示

        Returns:
            结果的字符串表示
        """
        return f"{self.full_path} {'(文件夹)' if self.is_folder else ''}"

    def __repr__(self) -> str:
        """对象表示

        Returns:
            对象的字符串表示
        """
        return f"FileResult(name='{self.name}', path='{self.path}', is_file={self.is_file})"


class ResultSet:
    """搜索结果集合，负责从Everything中获取和处理搜索结果"""

    def __init__(
        self, dll, max_results: Optional[int] = None, convert_date: bool = True
    ):
        """初始化结果集

        Args:
            dll: Everything DLL实例
            max_results: 最大结果数量，None表示所有结果
            convert_date: 是否将时间转换为datetime对象，False则使用字符串
        """
        self._dll = dll
        self._convert_date = convert_date

        self._total_results = dll.Everything_GetNumResults()
        self._total_files = dll.Everything_GetTotFileResults()
        self._total_folders = dll.Everything_GetTotFolderResults()

        self._max_results = (
            max_results if max_results is not None else self._total_results
        )

    def __len__(self) -> int:
        """结果数量

        Returns:
            结果集中的项目数量
        """
        return min(self._total_results, self._max_results)

    def __iter__(self) -> Iterator[FileResult]:
        """迭代结果集"""
        for i in range(min(self._total_results, self._max_results)):
            try:
                result = self._get_result_item(i)
                if result:
                    yield result
            except Exception as e:
                if DEBUG:
                    print(f"处理结果项 {i} 时出错: {e}")
                continue  # 跳过出错的项，继续处理下一项

    def _get_result_item(self, index: int) -> FileResult:
        """获取指定索引的结果

        Args:
            index: 结果索引

        Returns:
            FileResult对象
        """
        # 基本信息
        file_name = self._dll.Everything_GetResultFileNameW(index)
        path = self._dll.Everything_GetResultPathW(index)

        # 文件类型
        is_file = bool(self._dll.Everything_IsFileResult(index))
        is_folder = bool(self._dll.Everything_IsFolderResult(index))
        is_volume = bool(self._dll.Everything_IsVolumeResult(index))
        extension = self._dll.Everything_GetResultExtensionW(index)

        # 大小
        size = self._get_size(index)

        # 日期
        date_created = self._get_date_created(index)
        date_modified = self._get_date_modified(index)
        date_accessed = self._get_date_accessed(index)
        date_run = self._get_date_run(index)

        # 其他属性
        attributes = self._get_attributes(index)
        run_count = self._get_run_count(index)

        # 高亮信息
        highlighted_name = self._get_highlighted_name(index)
        highlighted_path = self._get_highlighted_path(index)

        return FileResult(
            name=file_name,
            path=path,
            size=size,
            date_created=date_created,
            date_modified=date_modified,
            date_accessed=date_accessed,
            date_run=date_run,
            extension=extension,
            attributes=attributes,
            is_file=is_file,
            is_folder=is_folder,
            is_volume=is_volume,
            run_count=run_count,
            highlighted_name=highlighted_name,
            highlighted_path=highlighted_path,
        )

    def _get_size(self, index: int) -> Optional[int]:
        """获取文件大小

        Args:
            index: 结果索引

        Returns:
            文件大小（字节）
        """
        buffer = ctypes.c_ulonglong(0)
        self._dll.Everything_GetResultSize(index, buffer)
        return buffer.value if buffer.value != 0xFFFFFFFFFFFFFFFF else None

    def _get_date_created(self, index: int) -> Optional[Union[datetime, str]]:
        """获取创建日期

        Args:
            index: 结果索引

        Returns:
            创建日期，格式取决于convert_date设置
        """
        try:
            buffer = ctypes.c_ulonglong(0)
            self._dll.Everything_GetResultDateCreated(index, buffer)

            if buffer.value == 0 or buffer.value == 0xFFFFFFFFFFFFFFFF:
                return None

            # 检查时间戳是否在有效范围内
            microsecs = (buffer.value - 116444736000000000.0) / 10000000.0
            current_time = time.time()
            if microsecs < 0 or microsecs > current_time + 3153600000:  # 现在+100年
                return None

            filetime = struct.pack("<Q", buffer.value)
            if self._convert_date:
                try:
                    return filetime_to_datetime(filetime)
                except Exception as e:
                    if DEBUG:
                        print(f"创建日期转换错误: {e}")
                    return None
            return filetime_to_str(filetime)
        except Exception as e:
            if DEBUG:
                print(f"获取创建日期错误: {e}")
            return None

    def _get_date_modified(self, index: int) -> Optional[Union[datetime, str]]:
        """获取修改日期

        Args:
            index: 结果索引

        Returns:
            修改日期，格式取决于convert_date设置
        """
        try:
            buffer = ctypes.c_ulonglong(0)
            self._dll.Everything_GetResultDateModified(index, buffer)

            if buffer.value == 0 or buffer.value == 0xFFFFFFFFFFFFFFFF:
                return None

            # 检查时间戳是否在有效范围内
            microsecs = (buffer.value - 116444736000000000.0) / 10000000.0
            current_time = time.time()
            if microsecs < 0 or microsecs > current_time + 3153600000:  # 现在+100年
                return None

            filetime = struct.pack("<Q", buffer.value)
            if self._convert_date:
                try:
                    return filetime_to_datetime(filetime)
                except Exception as e:
                    if DEBUG:
                        print(f"修改日期转换错误: {e}")
                    return None
            return filetime_to_str(filetime)
        except Exception as e:
            if DEBUG:
                print(f"获取修改日期错误: {e}")
            return None

    def _get_date_accessed(self, index: int) -> Optional[Union[datetime, str]]:
        """获取访问日期"""
        try:
            buffer = ctypes.c_ulonglong(0)
            self._dll.Everything_GetResultDateAccessed(index, buffer)

            # 调试输出
            if DEBUG:
                print(
                    f"winticks: {buffer.value}, microsecs: {(buffer.value - 116444736000000000.0) / 10000000.0}"
                )

            # 增加对无效值的检查
            if buffer.value == 0 or buffer.value == 0xFFFFFFFFFFFFFFFF:
                return None

            # 检查时间戳是否在有效范围内
            microsecs = (buffer.value - 116444736000000000.0) / 10000000.0
            current_time = time.time()
            if microsecs < 0 or microsecs > current_time + 3153600000:  # 现在+100年
                return None

            filetime = struct.pack("<Q", buffer.value)
            if self._convert_date:
                try:
                    return filetime_to_datetime(filetime)
                except Exception as e:
                    if DEBUG:
                        print(f"日期转换错误: {e}")
                    return None
            return filetime_to_str(filetime)
        except Exception as e:
            if DEBUG:
                print(f"获取访问日期错误: {e}")
            return None

    def _get_date_run(self, index: int) -> Optional[Union[datetime, str]]:
        """获取运行日期

        Args:
            index: 结果索引

        Returns:
            运行日期，格式取决于convert_date设置
        """
        try:
            buffer = ctypes.c_ulonglong(0)
            self._dll.Everything_GetResultDateRun(index, buffer)

            if buffer.value == 0 or buffer.value == 0xFFFFFFFFFFFFFFFF:
                return None

            # 检查时间戳是否在有效范围内
            microsecs = (buffer.value - 116444736000000000.0) / 10000000.0
            current_time = time.time()
            if microsecs < 0 or microsecs > current_time + 3153600000:  # 现在+100年
                return None

            filetime = struct.pack("<Q", buffer.value)
            if self._convert_date:
                try:
                    return filetime_to_datetime(filetime)
                except Exception as e:
                    if DEBUG:
                        print(f"运行日期转换错误: {e}")
                    return None
            return filetime_to_str(filetime)
        except Exception as e:
            if DEBUG:
                print(f"获取运行日期错误: {e}")
            return None

    def _get_attributes(self, index: int) -> int:
        """获取文件属性

        Args:
            index: 结果索引

        Returns:
            文件属性位掩码
        """
        return self._dll.Everything_GetResultAttributes(index)

    def _get_run_count(self, index: int) -> int:
        """获取运行次数

        Args:
            index: 结果索引

        Returns:
            运行次数
        """
        return self._dll.Everything_GetResultRunCount(index)

    def _get_highlighted_name(self, index: int) -> Optional[str]:
        """获取高亮文件名

        Args:
            index: 结果索引

        Returns:
            高亮的文件名
        """
        return self._dll.Everything_GetResultHighlightedFileNameW(index)

    def _get_highlighted_path(self, index: int) -> Optional[str]:
        """获取高亮路径

        Args:
            index: 结果索引

        Returns:
            高亮的路径
        """
        return self._dll.Everything_GetResultHighlightedPathW(index)

    def to_list(self) -> List[Dict[str, Any]]:
        """将结果集转换为字典列表

        Returns:
            字典列表
        """
        return [item.to_dict() for item in self]

    @property
    def total_results(self) -> int:
        """结果总数

        Returns:
            总结果数
        """
        return self._total_results

    @property
    def total_files(self) -> int:
        """文件总数

        Returns:
            文件总数
        """
        return self._total_files

    @property
    def total_folders(self) -> int:
        """文件夹总数

        Returns:
            文件夹总数
        """
        return self._total_folders

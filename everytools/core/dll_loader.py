#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DLL加载器模块
DLL loader module
"""

import os
import ctypes
import platform
from typing import Union, Optional, Dict, Any

from ..exceptions import DLLNotFoundError, EverythingError, raise_for_error_code
from ..utils.download import download_sdk_dll, get_architecture
from ..constants import RequestFlag, ErrorCode


class DLLLoader:
    """Everything SDK DLL加载和管理类"""

    def __init__(self, machine: Optional[int] = None):
        """初始化DLL加载器

        Args:
            machine: 系统架构(32或64)，如果不指定，将自动检测
        """
        self.machine = machine if machine is not None else get_architecture()
        self.everything_dll = self._load_dll()
        self._setup_function_types()

        # 获取版本信息
        self.major_version = self.everything_dll.Everything_GetMajorVersion()
        self.minor_version = self.everything_dll.Everything_GetMinorVersion()
        self.revision = self.everything_dll.Everything_GetRevision()
        self.build_number = self.everything_dll.Everything_GetBuildNumber()
        self.version = f"{self.major_version}.{self.minor_version}.{self.revision}.{self.build_number}"

    def _load_dll(self) -> Any:
        """加载Everything DLL

        Returns:
            加载的DLL对象

        Raises:
            DLLNotFoundError: 如果DLL无法加载
        """
        # 确定DLL路径
        if self.machine == 64:
            dll_name = "Everything64.dll"
        else:
            dll_name = "Everything32.dll"

        dll_dir = os.path.join(
            os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "dll"
        )
        dll_path = os.path.join(dll_dir, dll_name)

        # 如果DLL不存在，尝试下载
        if not os.path.exists(dll_path):
            try:
                download_sdk_dll(dll_dir)
            except Exception as e:
                raise DLLNotFoundError(f"无法下载Everything DLL: {str(e)}")

        # 尝试加载DLL
        try:
            return ctypes.WinDLL(dll_path)
        except Exception as e:
            raise DLLNotFoundError(f"无法加载Everything DLL: {str(e)}")

    def _setup_function_types(self) -> None:
        """设置DLL函数的参数和返回类型"""
        # 设置获取结果的函数类型
        self.everything_dll.Everything_GetResultDateCreated.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self.everything_dll.Everything_GetResultDateModified.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self.everything_dll.Everything_GetResultDateAccessed.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self.everything_dll.Everything_GetResultDateRun.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self.everything_dll.Everything_GetResultDateRecentlyChanged.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self.everything_dll.Everything_GetResultSize.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]

        # 设置异步查询函数类型
        self.everything_dll.Everything_IsQueryReply.argtypes = [
            ctypes.c_uint,
            ctypes.c_ulonglong,
            ctypes.c_ulonglong,
            ctypes.c_ulong,
        ]
        self.everything_dll.Everything_IsQueryReply.restype = ctypes.c_bool

        # 设置返回字符串的函数类型
        self.everything_dll.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
        self.everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p

        self.everything_dll.Everything_GetResultPathW.argtypes = [ctypes.c_int]
        self.everything_dll.Everything_GetResultPathW.restype = ctypes.c_wchar_p

        self.everything_dll.Everything_GetResultExtensionW.argtypes = [ctypes.c_int]
        self.everything_dll.Everything_GetResultExtensionW.restype = ctypes.c_wchar_p

        self.everything_dll.Everything_GetResultHighlightedFileNameW.argtypes = [
            ctypes.c_int
        ]
        self.everything_dll.Everything_GetResultHighlightedFileNameW.restype = (
            ctypes.c_wchar_p
        )

        self.everything_dll.Everything_GetResultHighlightedPathW.argtypes = [
            ctypes.c_int
        ]
        self.everything_dll.Everything_GetResultHighlightedPathW.restype = (
            ctypes.c_wchar_p
        )

        self.everything_dll.Everything_GetResultHighlightedFullPathAndFileNameW.argtypes = [
            ctypes.c_int
        ]
        self.everything_dll.Everything_GetResultHighlightedFullPathAndFileNameW.restype = (
            ctypes.c_wchar_p
        )

        self.everything_dll.Everything_GetSearchW.restype = ctypes.c_wchar_p

        # 设置完整路径函数类型
        self.everything_dll.Everything_GetResultFullPathNameW.argtypes = [ctypes.c_int]
        self.everything_dll.Everything_GetResultFullPathNameW.restype = ctypes.c_wchar_p

        # 设置文件列表文件名函数类型
        self.everything_dll.Everything_GetResultFileListFileNameW.argtypes = [
            ctypes.c_int
        ]
        self.everything_dll.Everything_GetResultFileListFileNameW.restype = (
            ctypes.c_wchar_p
        )

        # 设置运行历史相关函数类型
        self.everything_dll.Everything_GetRunCountFromFileNameW.argtypes = [
            ctypes.c_wchar_p
        ]
        self.everything_dll.Everything_GetRunCountFromFileNameW.restype = ctypes.c_ulong

        self.everything_dll.Everything_SetRunCountFromFileNameW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_ulong,
        ]
        self.everything_dll.Everything_SetRunCountFromFileNameW.restype = ctypes.c_bool

        self.everything_dll.Everything_IncRunCountFromFileNameW.argtypes = [
            ctypes.c_wchar_p
        ]
        self.everything_dll.Everything_IncRunCountFromFileNameW.restype = ctypes.c_ulong

        # 设置回调窗口相关函数类型
        self.everything_dll.Everything_SetReplyWindow.argtypes = [ctypes.c_void_p]
        self.everything_dll.Everything_SetReplyID.argtypes = [ctypes.c_ulong]
        self.everything_dll.Everything_GetReplyWindow.restype = ctypes.c_void_p
        self.everything_dll.Everything_GetReplyID.restype = ctypes.c_ulong

    def check_error(self) -> None:
        """检查并处理错误代码

        Raises:
            相应的异常类型
        """
        error_code = self.everything_dll.Everything_GetLastError()
        raise_for_error_code(error_code)

    def is_db_loaded(self) -> bool:
        """检查Everything数据库是否已加载

        Returns:
            布尔值表示数据库是否已加载
        """
        return bool(self.everything_dll.Everything_IsDBLoaded())

    def is_admin(self) -> bool:
        """检查Everything是否以管理员身份运行

        Returns:
            布尔值表示是否为管理员
        """
        return bool(self.everything_dll.Everything_IsAdmin())


# 单例模式，保证只有一个DLL加载器实例
_dll_loader_instance = None


def get_dll_loader(machine: Optional[int] = None) -> DLLLoader:
    """获取DLL加载器实例

    Args:
        machine: 系统架构(32或64)，如果不指定，将自动检测

    Returns:
        DLLLoader实例
    """
    global _dll_loader_instance
    if _dll_loader_instance is None:
        _dll_loader_instance = DLLLoader(machine)
    return _dll_loader_instance

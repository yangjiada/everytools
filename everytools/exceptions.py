#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Everything SDK 异常模块
Exception module for Everything SDK
"""

from .constants import ErrorCode


class EverythingError(Exception):
    """Everything搜索操作中的一般错误"""

    pass


class DLLNotFoundError(EverythingError):
    """无法找到或加载Everything DLL时的错误"""

    pass


class MemoryError(EverythingError):
    """内存分配错误"""

    pass


class IPCError(EverythingError):
    """IPC通信错误"""

    pass


class RegisterClassError(EverythingError):
    """注册窗口类错误"""

    pass


class CreateWindowError(EverythingError):
    """创建窗口错误"""

    pass


class CreateThreadError(EverythingError):
    """创建线程错误"""

    pass


class InvalidIndexError(EverythingError):
    """无效索引错误"""

    pass


class InvalidCallError(EverythingError):
    """无效调用错误"""

    pass


# 错误代码到异常类的映射
ERROR_CODE_TO_EXCEPTION = {
    ErrorCode.EVERYTHING_ERROR_MEMORY: MemoryError,
    ErrorCode.EVERYTHING_ERROR_IPC: IPCError,
    ErrorCode.EVERYTHING_ERROR_REGISTERCLASSEX: RegisterClassError,
    ErrorCode.EVERYTHING_ERROR_CREATEWINDOW: CreateWindowError,
    ErrorCode.EVERYTHING_ERROR_CREATETHREAD: CreateThreadError,
    ErrorCode.EVERYTHING_ERROR_INVALIDINDEX: InvalidIndexError,
    ErrorCode.EVERYTHING_ERROR_INVALIDCALL: InvalidCallError,
}


def raise_for_error_code(error_code):
    """根据错误代码抛出相应的异常

    Args:
        error_code: SDK返回的错误代码

    Raises:
        相应的异常类型
    """
    if error_code == ErrorCode.EVERYTHING_OK:
        return

    exception_class = ERROR_CODE_TO_EXCEPTION.get(error_code, EverythingError)
    raise exception_class(f"Everything SDK错误: {error_code}")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Everything SDK 常量定义模块
Constants module for Everything SDK
"""

from enum import IntEnum, IntFlag


class ErrorCode(IntEnum):
    """错误码枚举 (Error code enumeration)"""

    EVERYTHING_OK = 0  # 没有错误 (No error)
    EVERYTHING_ERROR_MEMORY = 1  # 内存错误 (Out of memory)
    EVERYTHING_ERROR_IPC = 2  # IPC通信错误 (IPC error)
    EVERYTHING_ERROR_REGISTERCLASSEX = 3  # 注册类错误 (RegisterClassEx failed)
    EVERYTHING_ERROR_CREATEWINDOW = 4  # 创建窗口错误 (CreateWindow failed)
    EVERYTHING_ERROR_CREATETHREAD = 5  # 创建线程错误 (CreateThread failed)
    EVERYTHING_ERROR_INVALIDINDEX = 6  # 索引无效 (Invalid index)
    EVERYTHING_ERROR_INVALIDCALL = 7  # 无效调用 (Invalid call)


class RequestFlag(IntFlag):
    """请求标志位枚举 (Request flag enumeration)"""

    FILE_NAME = 0x00000001  # 文件名 (File name)
    PATH = 0x00000002  # 路径 (Path)
    FULL_PATH_AND_FILE_NAME = 0x00000004  # 完整路径和文件名 (Full path and file name)
    EXTENSION = 0x00000008  # 扩展名 (Extension)
    SIZE = 0x00000010  # 大小 (Size)
    DATE_CREATED = 0x00000020  # 创建日期 (Date created)
    DATE_MODIFIED = 0x00000040  # 修改日期 (Date modified)
    DATE_ACCESSED = 0x00000080  # 访问日期 (Date accessed)
    ATTRIBUTES = 0x00000100  # 属性 (Attributes)
    FILE_LIST_FILE_NAME = 0x00000200  # 文件列表文件名 (File list file name)
    RUN_COUNT = 0x00000400  # 运行次数 (Run count)
    DATE_RUN = 0x00000800  # 运行日期 (Date run)
    DATE_RECENTLY_CHANGED = 0x00001000  # 最近更改日期 (Date recently changed)
    HIGHLIGHTED_FILE_NAME = 0x00002000  # 高亮文件名 (Highlighted file name)
    HIGHLIGHTED_PATH = 0x00004000  # 高亮路径 (Highlighted path)
    HIGHLIGHTED_FULL_PATH_AND_FILE_NAME = (
        0x00008000  # 高亮完整路径和文件名 (Highlighted full path and file name)
    )


class SortType(IntEnum):
    """排序类型枚举 (Sort type enumeration)"""

    NAME_ASCENDING = 1  # 名称升序 (Name ascending)
    NAME_DESCENDING = 2  # 名称降序 (Name descending)
    PATH_ASCENDING = 3  # 路径升序 (Path ascending)
    PATH_DESCENDING = 4  # 路径降序 (Path descending)
    SIZE_ASCENDING = 5  # 大小升序 (Size ascending)
    SIZE_DESCENDING = 6  # 大小降序 (Size descending)
    EXTENSION_ASCENDING = 7  # 扩展名升序 (Extension ascending)
    EXTENSION_DESCENDING = 8  # 扩展名降序 (Extension descending)
    TYPE_NAME_ASCENDING = 9  # 类型名称升序 (Type name ascending)
    TYPE_NAME_DESCENDING = 10  # 类型名称降序 (Type name descending)
    DATE_CREATED_ASCENDING = 11  # 创建日期升序 (Date created ascending)
    DATE_CREATED_DESCENDING = 12  # 创建日期降序 (Date created descending)
    DATE_MODIFIED_ASCENDING = 13  # 修改日期升序 (Date modified ascending)
    DATE_MODIFIED_DESCENDING = 14  # 修改日期降序 (Date modified descending)
    ATTRIBUTES_ASCENDING = 15  # 属性升序 (Attributes ascending)
    ATTRIBUTES_DESCENDING = 16  # 属性降序 (Attributes descending)
    FILE_LIST_FILENAME_ASCENDING = (
        17  # 文件列表文件名升序 (File list filename ascending)
    )
    FILE_LIST_FILENAME_DESCENDING = (
        18  # 文件列表文件名降序 (File list filename descending)
    )
    RUN_COUNT_ASCENDING = 19  # 运行次数升序 (Run count ascending)
    RUN_COUNT_DESCENDING = 20  # 运行次数降序 (Run count descending)
    DATE_RECENTLY_CHANGED_ASCENDING = (
        21  # 最近更改日期升序 (Date recently changed ascending)
    )
    DATE_RECENTLY_CHANGED_DESCENDING = (
        22  # 最近更改日期降序 (Date recently changed descending)
    )
    DATE_ACCESSED_ASCENDING = 23  # 访问日期升序 (Date accessed ascending)
    DATE_ACCESSED_DESCENDING = 24  # 访问日期降序 (Date accessed descending)
    DATE_RUN_ASCENDING = 25  # 运行日期升序 (Date run ascending)
    DATE_RUN_DESCENDING = 26  # 运行日期降序 (Date run descending)


class FileAttribute(IntFlag):
    """文件属性标志位 (File attribute flags)"""

    READONLY = 0x00000001  # 只读 (Read-only)
    HIDDEN = 0x00000002  # 隐藏 (Hidden)
    SYSTEM = 0x00000004  # 系统 (System)
    DIRECTORY = 0x00000010  # 目录 (Directory)
    ARCHIVE = 0x00000020  # 存档 (Archive)
    DEVICE = 0x00000040  # 设备 (Device)
    NORMAL = 0x00000080  # 正常 (Normal)
    TEMPORARY = 0x00000100  # 临时 (Temporary)
    SPARSE_FILE = 0x00000200  # 稀疏文件 (Sparse file)
    REPARSE_POINT = 0x00000400  # 重解析点 (Reparse point)
    COMPRESSED = 0x00000800  # 压缩 (Compressed)
    OFFLINE = 0x00001000  # 离线 (Offline)
    NOT_CONTENT_INDEXED = 0x00002000  # 未索引内容 (Not content indexed)
    ENCRYPTED = 0x00004000  # 加密 (Encrypted)

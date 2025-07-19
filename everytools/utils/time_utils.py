#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
时间处理工具模块
Time utility module
"""

import datetime
import struct
import time
from typing import Optional, Union

# 调试开关
DEBUG = False

# Windows文件时间常量
WINDOWS_TICKS = int(1 / 10**-7)  # 10,000,000 (100纳秒)
WINDOWS_EPOCH = datetime.datetime(1601, 1, 1)
POSIX_EPOCH = datetime.datetime(1970, 1, 1)
EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()  # 11644473600.0
WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS  # 116444736000000000.0

# 最大Windows时间值表示"未知"
MAX_WINDOWS_TICKS = 0xFFFFFFFFFFFFFFFF


def filetime_to_datetime(filetime: bytes) -> Optional[datetime.datetime]:
    """将Windows文件时间转换为Python datetime对象"""
    try:
        winticks = struct.unpack("<Q", filetime)[0]

        # 调试输出
        if DEBUG:
            print(
                f"winticks: {winticks}, microsecs: {(winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS}"
            )

        # 处理特殊情况：0值或最大值
        if winticks == 0 or winticks == MAX_WINDOWS_TICKS:
            return None

        # 确保时间戳大于Windows时间起点且在合理范围内
        if winticks <= WINDOWS_TICKS_TO_POSIX_EPOCH:
            return None

        microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS

        # 检查时间戳是否在有效范围内（1970-01-01 到 现在+100年）
        current_time = time.time()
        if microsecs < 0 or microsecs > current_time + 3153600000:  # 现在+100年
            return None

        # 避免无效时间戳
        return datetime.datetime.fromtimestamp(microsecs)
    except (ValueError, OSError, OverflowError, struct.error) as e:
        # 调试输出
        if DEBUG:
            print(f"时间转换错误: {e}")
        return None


def filetime_to_timestamp(filetime: bytes) -> Optional[float]:
    """将Windows文件时间转换为Unix时间戳"""
    try:
        winticks = struct.unpack("<Q", filetime)[0]

        # 处理特殊情况：0值或最大值
        if winticks == 0 or winticks == MAX_WINDOWS_TICKS:
            return None

        # 确保时间戳大于Windows时间起点
        if winticks <= WINDOWS_TICKS_TO_POSIX_EPOCH:
            return None

        microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS

        # 检查时间戳是否在有效范围内
        if microsecs < 0 or microsecs > time.time() + 3153600000:  # 现在+100年
            return None

        return microsecs
    except (struct.error, OverflowError):
        return None


def filetime_to_str(
    filetime: bytes, format_str: str = "%Y-%m-%d %H:%M:%S"
) -> Optional[str]:
    """将Windows文件时间转换为格式化的时间字符串

    Args:
        filetime: Windows FILETIME结构体的字节表示
        format_str: 格式化字符串，默认为"%Y-%m-%d %H:%M:%S"

    Returns:
        格式化的时间字符串，如果是最大值表示未知，则返回None
    """
    try:
        timestamp = filetime_to_timestamp(filetime)

        if timestamp is None:
            return None

        return time.strftime(format_str, time.localtime(timestamp))
    except (ValueError, OSError, OverflowError):
        return None


def datetime_to_filetime(dt: Union[datetime.datetime, float, None]) -> bytes:
    """将Python datetime或时间戳转换为Windows文件时间

    Args:
        dt: datetime对象或Unix时间戳，None表示未知

    Returns:
        Windows FILETIME结构体的字节表示
    """
    if dt is None:
        return struct.pack("<Q", MAX_WINDOWS_TICKS)

    if isinstance(dt, datetime.datetime):
        # 转换datetime为秒数
        timestamp = dt.timestamp()
    else:
        # 直接使用时间戳
        timestamp = dt

    winticks = int(timestamp * WINDOWS_TICKS + WINDOWS_TICKS_TO_POSIX_EPOCH)
    return struct.pack("<Q", winticks)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
下载工具模块
Download utility module
"""

import os
import zipfile
import platform
from typing import Optional

import requests


class DownloadError(Exception):
    """下载过程中发生的错误"""

    pass


def download_sdk_dll(dll_dir: str) -> None:
    """下载Everything-SDK.zip，并解压DLL到指定目录

    Args:
        dll_dir: DLL文件的保存目录

    Raises:
        DownloadError: 下载或解压过程中发生错误
    """
    os.makedirs(dll_dir, exist_ok=True)
    url = "https://www.voidtools.com/Everything-SDK.zip"

    try:
        print(f"正在从 {url} 下载Everything SDK...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # 检查HTTP错误

        temp_zip = os.path.join(dll_dir, "Everything-SDK.zip")
        with open(temp_zip, "wb") as f:
            f.write(response.content)

        print(f"正在解压DLL到 {dll_dir}...")
        with zipfile.ZipFile(temp_zip, "r") as zip_ref:
            for name in zip_ref.namelist():
                if name.endswith(".dll"):
                    content = zip_ref.read(name)
                    dll_name = os.path.basename(name)
                    with open(os.path.join(dll_dir, dll_name), "wb") as f:
                        f.write(content)

        # 删除临时ZIP文件
        os.remove(temp_zip)
        print("下载和解压完成")
    except requests.RequestException as e:
        raise DownloadError(f"下载SDK失败: {str(e)}")
    except zipfile.BadZipFile:
        if os.path.exists(temp_zip):
            os.remove(temp_zip)
        raise DownloadError("无效的ZIP文件")
    except Exception as e:
        raise DownloadError(f"处理SDK过程中出错: {str(e)}")


def get_architecture() -> int:
    """获取系统架构（32位或64位）

    Returns:
        32或64表示系统位数
    """
    return 64 if platform.architecture()[0] == "64bit" else 32

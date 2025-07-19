#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : Jan Yang
@software: PyCharm Community Edition
@Email : yang.jiada@foxmail.com
"""
import datetime
import time
import struct
import ctypes
import math
import os
import requests
import zipfile
from .constants import RequestFlag, SortType

# convert a windows FILETIME to a python datetime
# https://stackoverflow.com/questions/39481221/convert-datetime-back-to-windows-64-bit-filetime
WINDOWS_TICKS = int(1 / 10**-7)  # 10,000,000 (100 nanoseconds or .1 microseconds)
WINDOWS_EPOCH = datetime.datetime.strptime("1601-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
POSIX_EPOCH = datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()  # 11644473600.0
WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS  # 116444736000000000.0


def get_time(filetime):
    """Convert windows filetime winticks to python datetime.datetime."""
    winticks = struct.unpack("<Q", filetime)[0]
    microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(microsecs))
    except OSError:
        return None


def download_dll(dll_dir):
    """下载Everything-SDK.zip，并解压到dll_dir"""
    os.makedirs(dll_dir, exist_ok=True)
    url = "https://www.voidtools.com/Everything-SDK.zip"
    print(f"downloading dll from {url}")
    response = requests.get(url)
    with open("Everything-SDK.zip", "wb") as f:
        f.write(response.content)
    print(f"extracting dll to {dll_dir}")
    with zipfile.ZipFile("Everything-SDK.zip", "r") as zip_ref:
        for name in zip_ref.namelist():
            if name.endswith(".dll"):
                content = zip_ref.read(name)
                with open(os.path.join(dll_dir, os.path.basename(name)), "wb") as f:
                    f.write(content)
    os.remove("Everything-SDK.zip")
    print("done")


# 重复的枚举定义已移至constants.py，这里直接使用导入的版本


class EveryTools:
    def __init__(self, machine=64):
        self.machine = machine

        # dll导入
        if self.machine == 64:
            dll_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "dll", "Everything64.dll"
            )
        elif self.machine == 32:
            dll_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "dll", "Everything32.dll"
            )
        else:
            dll_path = None

        if not os.path.exists(dll_path):
            download_dll(os.path.dirname(dll_path))

        self.everything_dll = ctypes.WinDLL(dll_path)

        # 定义数据类型
        self.everything_dll.Everything_GetResultDateCreated.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self.everything_dll.Everything_GetResultDateModified.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self.everything_dll.Everything_GetResultSize.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self.everything_dll.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
        self.everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p
        self.everything_dll.Everything_GetResultPathW.restype = ctypes.c_wchar_p
        self.everything_dll.Everything_GetResultExtensionW.restype = ctypes.c_wchar_p

        # 版本信息
        self.major_version = self.everything_dll.Everything_GetMajorVersion()
        self.minor_version = self.everything_dll.Everything_GetMinorVersion()
        self.revision = self.everything_dll.Everything_GetRevision()
        self.build_number = self.everything_dll.Everything_GetBuildNumber()
        self.version = f"{self.major_version}.{self.minor_version}.{self.revision}.{self.build_number}"

        # 搜索结果信息
        self.num_total_results = 0
        self.num_total_file = 0
        self.num_total_folder = 0

    def search(
        self, keywords, math_path=False, math_case=False, whole_world=False, regex=False
    ):
        """基本搜索

        :param keywords: 关键词
        :param math_path: 匹配路径
        :param math_case: 区分大小写
        :param whole_world: 全字匹配
        :param regex: 使用正则
        :return:
        """

        # self.everything_dll.Everything_CleanUp()
        self.everything_dll.Everything_Reset()  # 重置状态
        self.everything_dll.Everything_SetSearchW(keywords)
        self.everything_dll.Everything_SetMatchPath(math_path)  # 匹配路径
        self.everything_dll.Everything_SetMatchCase(math_case)  # 区分大小写
        self.everything_dll.Everything_SetMatchWholeWord(whole_world)  # 全字匹配
        self.everything_dll.Everything_SetRegex(regex)  # 使用正则表达式

        # self.everything_dll.Everything_SetReplyWindow(0)
        # self.everything_dll.Everything_SetReplyID(0)
        # 执行查询
        self.everything_dll.Everything_QueryW(True)

        # 获取搜索结果
        self.num_total_results = self.everything_dll.Everything_GetNumResults()
        self.num_total_file = self.everything_dll.Everything_GetTotFileResults()
        self.num_total_folder = self.everything_dll.Everything_GetTotFolderResults()

    def get_search_keyword(self):
        """获取搜索关键词

        :return: string
        """
        self.everything_dll.Everything_GetSearchW.restype = ctypes.c_wchar_p
        return self.everything_dll.Everything_GetSearchW()

    def get_num_total_results(self):
        """获取全部结果数量

        :return:
        """
        return self.num_total_results

    def get_num_total_file(self):
        """获取全部'文件'结果数量

        :return:
        """
        return self.num_total_file

    def get_num_total_folder(self):
        """获取全部'文件夹'结果数量

        :return:
        """
        return self.num_total_folder

    def search_audio(self, keywords=""):
        """搜索音频文件

        :param keywords: 关键词
        :return:
        """
        self.search(
            f"ext:aac;ac3;aif;aifc;aiff;au;cda;dts;fla;flac;it;m1a;m2a;m3u;m4a;mid;midi;mka;mod;mp2;mp3;mpa;"
            f"ogg;ra;rmi;spc;rmi;snd;umx;voc;wav;wma;xm {keywords}"
        )

    def search_zip(self, keywords=""):
        """搜索压缩文件

        :param keywords: 关键词
        :return:
        """
        self.search(
            f"ext:7z;ace;arj;bz2;cab;gz;gzip;jar;r00;r01;r02;r03;r04;r05;r06;r07;r08;r09;r10;r11;r12;r13;r14;"
            f"r15;r16;r17;r18;r19;r20;r21;r22;r23;r24;r25;r26;r27;r28;r29;rar;tar;tgz;z;zip {keywords}"
        )

    def search_doc(self, keywords=""):
        """搜索文档

        :param keywords: 关键词
        :return:
        """
        self.search(
            f"ext:c;chm;cpp;csv;cxx;doc;docm;docx;dot;dotm;dotx;h;hpp;htm;html;hxx;ini;java;lua;mht;mhtml;"
            f"odt;pdf;potx;potm;ppam;ppsm;ppsx;pps;ppt;pptm;pptx;rtf;sldm;sldx;thmx;txt;vsd;wpd;wps;wri;"
            f"xlam;xls;xlsb;xlsm;xlsx;xltm;xltx;xml {keywords}"
        )

    def search_exe(self, keywords=""):
        """搜索可执行文件

        :param keywords: 关键词
        :return:
        """
        self.search(f"ext:bat;cmd;exe;msi;msp;scr {keywords}")

    def search_folder(self, keywords=""):
        """搜索文件夹

        :param keywords: 关键词
        :return:
        """
        self.search(f"folder: {keywords}")

    def search_pic(self, keywords=""):
        """搜索图片

        :param keywords: 关键词
        :return:
        """
        self.search(
            f"ext:ani;bmp;gif;ico;jpe;jpeg;jpg;pcx;png;psd;tga;tif;tiff;webp;wmf {keywords}"
        )

    def search_video(self, keywords=""):
        """搜索视频

        :param keywords: 关键词
        :return:
        """
        self.search(
            f"ext:3g2;3gp;3gp2;3gpp;amr;amv;asf;avi;bdmv;bik;d2v;divx;drc;dsa;dsm;dss;dsv;evo;f4v;flc;fli;"
            f"flic;flv;hdmov;ifo;ivf;m1v;m2p;m2t;m2ts;m2v;m4b;m4p;m4v;mkv;mp2v;mp4;mp4v;mpe;mpeg;mpg;mpls;"
            f"mpv2;mpv4;mov;mts;ogm;ogv;pss;pva;qt;ram;ratdvd;rm;rmm;rmvb;roq;rpm;smil;smk;swf;tp;tpr;ts;"
            f"vob;vp6;webm;wm;wmp;wmv {keywords}"
        )

    def search_ext(self, ext, keywords=""):
        """搜索扩展名称

        :param ext: 拓展名
        :param keywords: 关键词
        :return:
        """
        self.search(f"ext:{ext} {keywords}")

    def search_in_located(self, path, keywords=""):
        """搜索路径下文件

        :param path: 搜索的路径
        :param keywords: 关键词
        :return:
        """
        self.search(f"{path} {keywords}")

    def results(self, max_num=None, sort_type=1):
        """输出结果

        :param max_num: 最大数量
        :param sort_type: 排序类型
        :return: iterator of result dict
        """
        # 定义块数据
        buffer_full_path_name = ctypes.create_unicode_buffer(260)
        buffer_created_time = ctypes.c_ulonglong(1)
        buffer_modified_time = ctypes.c_ulonglong(1)
        buffer_size = ctypes.c_ulonglong(1)

        # 设置排序
        self.everything_dll.Everything_SetSort(sort_type)

        num_total = self.get_num_total_results()  # 获取全部结果数量
        if max_num and max_num < num_total:
            num_total = max_num

        if num_total == 0:
            return

        #  | EVERYTHING_REQUEST_ATTRIBUTES
        self.everything_dll.Everything_SetRequestFlags(
            RequestFlag.FILE_NAME.value
            | RequestFlag.PATH.value
            | RequestFlag.SIZE.value
            | RequestFlag.DATE_CREATED.value
            | RequestFlag.DATE_MODIFIED.value
            | RequestFlag.EXTENSION.value
        )
        self.everything_dll.Everything_QueryW(True)
        # 不再需要分页逻辑，直接迭代
        for i in range(num_total):
            file_name = self.everything_dll.Everything_GetResultFileNameW(i)
            file_path = self.everything_dll.Everything_GetResultPathW(i)

            # 创建时间
            self.everything_dll.Everything_GetResultDateCreated(i, buffer_created_time)
            if struct.unpack("<Q", buffer_created_time)[0] == 18446744073709551615:
                created_time = None
            else:
                created_time = get_time(buffer_created_time)

            # 获取查询信息
            self.everything_dll.Everything_GetResultDateModified(
                i, buffer_modified_time
            )
            modified_time = get_time(buffer_modified_time)
            self.everything_dll.Everything_GetResultSize(i, buffer_size)  # 大小
            file_size = buffer_size.value
            file_extension = self.everything_dll.Everything_GetResultExtensionW(
                i
            )  # 拓展
            is_file = self.everything_dll.Everything_IsFileResult(i)
            is_folder = self.everything_dll.Everything_IsFolderResult(i)
            is_volume = self.everything_dll.Everything_IsVolumeResult(i)

            item = {
                "name": file_name,
                "path": file_path,
                "size": file_size,
                "created_date": created_time,
                "modified_date": modified_time,
                "file_extension": file_extension,
                "is_file": is_file,
                "is_folder": is_folder,
                "is_volume": is_volume,
            }

            yield item  # 使用yield返回，而不是append到列表

    def exit(self):
        """执行退出客户端操作，会失去连接"""
        self.everything_dll.Everything_Exit()

    def set_sort(self, sort_type):
        """设置搜索结果排序方式

        :param sort_type: 排序类型常量
        """
        self.everything_dll.Everything_SetSort(sort_type)

    def get_last_error(self):
        """获取最后一次错误

        :return: 错误代码
        """
        return self.everything_dll.Everything_GetLastError()

    def sort_results_by_path(self):
        """按路径排序结果"""
        self.everything_dll.Everything_SortResultsByPath()

    def is_db_loaded(self):
        """检查数据库是否已加载

        :return: 布尔值
        """
        return bool(self.everything_dll.Everything_IsDBLoaded())

    def is_admin(self):
        """检查是否为管理员

        :return: 布尔值
        """
        return bool(self.everything_dll.Everything_IsAdmin())


if __name__ == "__main__":
    et = EveryTools()
    # et.search("abcdefs")
    et.search_ext("pdf", "python")
    print("search keywords is:", et.get_search_keyword())
    print("get_num_total_results:", et.get_num_total_results())
    result = et.results()
    # print(list(result))  # 迭代器可以转为列表
    # print(et.is_admin())

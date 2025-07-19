#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Everything SDK完整API包装器
Complete API wrapper for Everything SDK
"""

import ctypes
from typing import Optional, Union
from .dll_loader import get_dll_loader
from ..constants import SortType, RequestFlag


class EverythingAPI:
    """Everything SDK完整API包装器"""

    def __init__(self, machine: Optional[int] = None):
        self._dll_loader = get_dll_loader(machine)
        self._dll = self._dll_loader.everything_dll

    # ========== 操作搜索状态 ==========

    def set_search(self, search: str) -> None:
        """设置搜索字符串"""
        self._dll.Everything_SetSearchW(search)

    def set_match_path(self, enable: bool) -> None:
        """设置是否匹配路径"""
        self._dll.Everything_SetMatchPath(enable)

    def set_match_case(self, enable: bool) -> None:
        """设置是否区分大小写"""
        self._dll.Everything_SetMatchCase(enable)

    def set_match_whole_word(self, enable: bool) -> None:
        """设置是否全字匹配"""
        self._dll.Everything_SetMatchWholeWord(enable)

    def set_regex(self, enable: bool) -> None:
        """设置是否使用正则表达式"""
        self._dll.Everything_SetRegex(enable)

    def set_max(self, max_results: int) -> None:
        """设置最大结果数量"""
        self._dll.Everything_SetMax(max_results)

    def set_offset(self, offset: int) -> None:
        """设置结果偏移量"""
        self._dll.Everything_SetOffset(offset)

    def set_sort(self, sort_type: Union[SortType, int]) -> None:
        """设置排序方式"""
        if isinstance(sort_type, SortType):
            sort_type = sort_type.value
        self._dll.Everything_SetSort(sort_type)

    def set_request_flags(self, flags: Union[RequestFlag, int]) -> None:
        """设置请求标志位"""
        if isinstance(flags, RequestFlag):
            flags = flags.value
        self._dll.Everything_SetRequestFlags(flags)

    # ========== 读取搜索状态 ==========

    def get_search(self) -> str:
        """获取搜索字符串"""
        self._dll.Everything_GetSearchW.restype = ctypes.c_wchar_p
        return self._dll.Everything_GetSearchW() or ""

    def get_match_path(self) -> bool:
        """获取是否匹配路径"""
        return bool(self._dll.Everything_GetMatchPath())

    def get_match_case(self) -> bool:
        """获取是否区分大小写"""
        return bool(self._dll.Everything_GetMatchCase())

    def get_match_whole_word(self) -> bool:
        """获取是否全字匹配"""
        return bool(self._dll.Everything_GetMatchWholeWord())

    def get_regex(self) -> bool:
        """获取是否使用正则表达式"""
        return bool(self._dll.Everything_GetRegex())

    def get_max(self) -> int:
        """获取最大结果数量"""
        return self._dll.Everything_GetMax()

    def get_offset(self) -> int:
        """获取结果偏移量"""
        return self._dll.Everything_GetOffset()

    def get_last_error(self) -> int:
        """获取最后一次错误代码"""
        return self._dll.Everything_GetLastError()

    def get_sort(self) -> int:
        """获取排序方式"""
        return self._dll.Everything_GetSort()

    def get_request_flags(self) -> int:
        """获取请求标志位"""
        return self._dll.Everything_GetRequestFlags()

    # ========== 执行查询 ==========

    def query(self, wait: bool = True) -> bool:
        """执行查询"""
        result = self._dll.Everything_QueryW(wait)
        if not result:
            self._dll_loader.check_error()
        return bool(result)

    # ========== 操作结果 ==========

    def sort_results_by_path(self) -> None:
        """按路径排序结果"""
        self._dll.Everything_SortResultsByPath()

    def reset(self) -> None:
        """重置搜索状态"""
        self._dll.Everything_Reset()

    # ========== 读取结果 ==========

    def get_num_file_results(self) -> int:
        """获取文件结果数量"""
        return self._dll.Everything_GetNumFileResults()

    def get_num_folder_results(self) -> int:
        """获取文件夹结果数量"""
        return self._dll.Everything_GetNumFolderResults()

    def get_num_results(self) -> int:
        """获取总结果数量"""
        return self._dll.Everything_GetNumResults()

    def get_tot_file_results(self) -> int:
        """获取总文件结果数量"""
        return self._dll.Everything_GetTotFileResults()

    def get_tot_folder_results(self) -> int:
        """获取总文件夹结果数量"""
        return self._dll.Everything_GetTotFolderResults()

    def get_tot_results(self) -> int:
        """获取总结果数量"""
        return self._dll.Everything_GetTotResults()

    def is_volume_result(self, index: int) -> bool:
        """检查指定索引是否为卷结果"""
        return bool(self._dll.Everything_IsVolumeResult(index))

    def is_folder_result(self, index: int) -> bool:
        """检查指定索引是否为文件夹结果"""
        return bool(self._dll.Everything_IsFolderResult(index))

    def is_file_result(self, index: int) -> bool:
        """检查指定索引是否为文件结果"""
        return bool(self._dll.Everything_IsFileResult(index))

    def get_result_file_name(self, index: int) -> str:
        """获取结果文件名"""
        result = self._dll.Everything_GetResultFileNameW(index)
        return result or ""

    def get_result_path(self, index: int) -> str:
        """获取结果路径"""
        result = self._dll.Everything_GetResultPathW(index)
        return result or ""

    def get_result_extension(self, index: int) -> str:
        """获取结果扩展名"""
        result = self._dll.Everything_GetResultExtensionW(index)
        return result or ""

    def get_result_size(self, index: int) -> int:
        """获取结果文件大小"""
        size = ctypes.c_ulonglong()
        self._dll.Everything_GetResultSize(index, ctypes.byref(size))
        return size.value

    def get_result_date_created(self, index: int) -> Optional[int]:
        """获取结果创建时间（Windows FILETIME格式）"""
        filetime = ctypes.c_ulonglong()
        self._dll.Everything_GetResultDateCreated(index, ctypes.byref(filetime))
        return filetime.value if filetime.value != 0 else None

    def get_result_date_modified(self, index: int) -> Optional[int]:
        """获取结果修改时间（Windows FILETIME格式）"""
        filetime = ctypes.c_ulonglong()
        self._dll.Everything_GetResultDateModified(index, ctypes.byref(filetime))
        return filetime.value if filetime.value != 0 else None

    def get_result_date_accessed(self, index: int) -> Optional[int]:
        """获取结果访问时间（Windows FILETIME格式）"""
        filetime = ctypes.c_ulonglong()
        self._dll.Everything_GetResultDateAccessed(index, ctypes.byref(filetime))
        return filetime.value if filetime.value != 0 else None

    def get_result_attributes(self, index: int) -> int:
        """获取结果文件属性"""
        return self._dll.Everything_GetResultAttributes(index)

    def get_result_full_path_name(self, index: int) -> str:
        """获取结果完整路径和文件名"""
        result = self._dll.Everything_GetResultFullPathNameW(index)
        return result or ""

    def get_result_run_count(self, index: int) -> int:
        """获取结果运行次数"""
        return self._dll.Everything_GetResultRunCount(index)

    def get_result_date_run(self, index: int) -> Optional[int]:
        """获取结果运行时间（Windows FILETIME格式）"""
        filetime = ctypes.c_ulonglong()
        self._dll.Everything_GetResultDateRun(index, ctypes.byref(filetime))
        return filetime.value if filetime.value != 0 else None

    def get_result_date_recently_changed(self, index: int) -> Optional[int]:
        """获取结果最近更改时间（Windows FILETIME格式）"""
        filetime = ctypes.c_ulonglong()
        self._dll.Everything_GetResultDateRecentlyChanged(index, ctypes.byref(filetime))
        return filetime.value if filetime.value != 0 else None

    def get_result_highlighted_file_name(self, index: int) -> str:
        """获取高亮显示的文件名"""
        result = self._dll.Everything_GetResultHighlightedFileNameW(index)
        return result or ""

    def get_result_highlighted_path(self, index: int) -> str:
        """获取高亮显示的路径"""
        result = self._dll.Everything_GetResultHighlightedPathW(index)
        return result or ""

    def get_result_highlighted_full_path_and_file_name(self, index: int) -> str:
        """获取高亮显示的完整路径和文件名"""
        result = self._dll.Everything_GetResultHighlightedFullPathAndFileNameW(index)
        return result or ""

    def get_result_list_sort(self) -> int:
        """获取结果列表排序方式"""
        return self._dll.Everything_GetResultListSort()

    def get_result_list_request_flags(self) -> int:
        """获取结果列表请求标志位"""
        return self._dll.Everything_GetResultListRequestFlags()

    def get_result_file_list_file_name(self, index: int) -> str:
        """获取结果文件列表文件名"""
        result = self._dll.Everything_GetResultFileListFileNameW(index)
        return result or ""

    # ========== 检查查询应答 ==========

    def is_query_reply(
        self, message: int, wparam: int, lparam: int, reply_id: int
    ) -> bool:
        """检查是否为查询应答消息"""
        return bool(
            self._dll.Everything_IsQueryReply(message, wparam, lparam, reply_id)
        )

    # ========== 设置回调窗口和ID ==========

    def set_reply_window(self, window_handle: int) -> None:
        """设置回复窗口句柄"""
        self._dll.Everything_SetReplyWindow(window_handle)

    def set_reply_id(self, reply_id: int) -> None:
        """设置回复ID"""
        self._dll.Everything_SetReplyID(reply_id)

    def get_reply_window(self) -> int:
        """获取回复窗口句柄"""
        return self._dll.Everything_GetReplyWindow()

    def get_reply_id(self) -> int:
        """获取回复ID"""
        return self._dll.Everything_GetReplyID()

    # ========== 运行历史 ==========

    def get_run_count_from_file_name(self, file_name: str) -> int:
        """从文件名获取运行次数"""
        return self._dll.Everything_GetRunCountFromFileNameW(file_name)

    def set_run_count_from_file_name(self, file_name: str, run_count: int) -> bool:
        """设置文件名的运行次数"""
        return bool(self._dll.Everything_SetRunCountFromFileNameW(file_name, run_count))

    def inc_run_count_from_file_name(self, file_name: str) -> int:
        """增加文件名的运行次数"""
        return self._dll.Everything_IncRunCountFromFileNameW(file_name)

    # ========== 常规功能 ==========

    def cleanup(self) -> None:
        """清理资源"""
        self._dll.Everything_CleanUp()

    def get_major_version(self) -> int:
        """获取主版本号"""
        return self._dll.Everything_GetMajorVersion()

    def get_minor_version(self) -> int:
        """获取次版本号"""
        return self._dll.Everything_GetMinorVersion()

    def get_revision(self) -> int:
        """获取修订版本号"""
        return self._dll.Everything_GetRevision()

    def get_build_number(self) -> int:
        """获取构建号"""
        return self._dll.Everything_GetBuildNumber()

    def exit(self) -> None:
        """退出Everything"""
        self._dll.Everything_Exit()

    def is_db_loaded(self) -> bool:
        """检查数据库是否已加载"""
        return bool(self._dll.Everything_IsDBLoaded())

    def is_admin(self) -> bool:
        """检查是否以管理员身份运行"""
        return bool(self._dll.Everything_IsAdmin())

    def is_app_data(self) -> bool:
        """检查是否使用应用数据"""
        return bool(self._dll.Everything_IsAppData())

    def rebuild_db(self) -> None:
        """重建数据库"""
        self._dll.Everything_RebuildDB()

    def update_all_folder_indexes(self) -> None:
        """更新所有文件夹索引"""
        self._dll.Everything_UpdateAllFolderIndexes()

    def save_db(self) -> None:
        """保存数据库"""
        self._dll.Everything_SaveDB()

    def save_run_history(self) -> None:
        """保存运行历史"""
        self._dll.Everything_SaveRunHistory()

    def delete_run_history(self) -> None:
        """删除运行历史"""
        self._dll.Everything_DeleteRunHistory()

    def get_target_machine(self) -> int:
        """获取目标机器架构"""
        return self._dll.Everything_GetTargetMachine()


# 单例实例
_api_instance = None


def get_api(machine: Optional[int] = None) -> EverythingAPI:
    """获取API实例"""
    global _api_instance
    if _api_instance is None:
        _api_instance = EverythingAPI(machine)
    return _api_instance

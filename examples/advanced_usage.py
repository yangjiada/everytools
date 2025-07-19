#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Everything SDK 高级使用示例
Advanced usage examples for Everything SDK
"""

from everytools.core.api_wrapper import get_api
from everytools.query.search import SearchBuilder
from everytools.query.filters import FileFilter, DateFilter, MediaFilter
from everytools.constants import SortType, RequestFlag


def basic_search_example():
    """基本搜索示例"""
    print("=== 基本搜索示例 ===")

    # 使用SearchBuilder进行搜索
    search = (
        SearchBuilder()
        .keywords("python")
        .match_case(False)
        .limit(5)
        .sort_by(SortType.SIZE_DESCENDING)
        .execute()
    )

    results = search.get_results()
    print(f"找到 {len(results)} 个结果:")

    for i, result in enumerate(results):
        print(f"{i+1}. {result.name}")
        print(f"   路径: {result.path}")
        print(f"   大小: {result.size} 字节")
        print(f"   修改时间: {result.date_modified}")
        print()


def advanced_filter_example():
    """高级过滤器示例"""
    print("=== 高级过滤器示例 ===")

    # 搜索大于1MB的PDF文档，按修改时间排序
    search = (
        SearchBuilder()
        .keywords("报告")
        .filter(
            FileFilter()
            .with_extensions("pdf", "docx")
            .with_size_range(min_size=1024 * 1024)  # >1MB
        )
        .filter(DateFilter().by_modified_date().in_range(start_date="2023-01-01"))
        .sort_by(SortType.DATE_MODIFIED_DESCENDING)
        .limit(10)
        .execute()
    )

    results = search.get_results()
    print(f"找到 {len(results)} 个符合条件的文档:")

    for result in results:
        size_mb = result.size / (1024 * 1024) if result.size else 0
        print(f"- {result.name} ({size_mb:.2f} MB)")
        print(f"  修改时间: {result.date_modified}")


def media_search_example():
    """媒体文件搜索示例"""
    print("=== 媒体文件搜索示例 ===")

    # 搜索音频文件
    audio_search = (
        SearchBuilder()
        .keywords("music")
        .filter(MediaFilter("audio"))
        .sort_by(SortType.SIZE_DESCENDING)
        .limit(5)
        .execute()
    )

    audio_results = audio_search.get_results()
    print(f"找到 {len(audio_results)} 个音频文件:")

    for result in audio_results:
        size_mb = result.size / (1024 * 1024) if result.size else 0
        print(f"- {result.name} ({size_mb:.2f} MB)")


def direct_api_example():
    """直接使用API的示例"""
    print("=== 直接API使用示例 ===")

    api = get_api()

    # 设置搜索参数
    api.set_search("*.txt")
    api.set_match_case(False)
    api.set_max(3)
    api.set_sort(SortType.NAME_ASCENDING)
    api.set_request_flags(
        RequestFlag.FILE_NAME
        | RequestFlag.PATH
        | RequestFlag.SIZE
        | RequestFlag.DATE_MODIFIED
    )

    # 执行查询
    if api.query():
        num_results = api.get_num_results()
        print(f"找到 {num_results} 个文本文件:")

        for i in range(min(num_results, 3)):
            name = api.get_result_file_name(i)
            path = api.get_result_path(i)
            size = api.get_result_size(i)

            print(f"{i+1}. {name}")
            print(f"   路径: {path}")
            print(f"   大小: {size} 字节")
    else:
        print("搜索失败")


def system_info_example():
    """系统信息示例"""
    print("=== 系统信息示例 ===")

    api = get_api()

    print(
        f"Everything版本: {api.get_major_version()}.{api.get_minor_version()}.{api.get_revision()}.{api.get_build_number()}"
    )
    print(f"数据库已加载: {'是' if api.is_db_loaded() else '否'}")
    print(f"管理员权限: {'是' if api.is_admin() else '否'}")
    print(f"使用应用数据: {'是' if api.is_app_data() else '否'}")
    print(f"目标架构: {api.get_target_machine()}")


def run_history_example():
    """运行历史示例"""
    print("=== 运行历史示例 ===")

    api = get_api()

    # 假设的文件路径
    test_file = "C:\\Windows\\notepad.exe"

    # 获取运行次数
    run_count = api.get_run_count_from_file_name(test_file)
    print(f"{test_file} 的运行次数: {run_count}")

    # 增加运行次数
    new_count = api.inc_run_count_from_file_name(test_file)
    print(f"增加后的运行次数: {new_count}")


def error_handling_example():
    """错误处理示例"""
    print("=== 错误处理示例 ===")

    try:
        api = get_api()

        # 设置一个可能导致错误的搜索
        api.set_search("regex:[[invalid")  # 无效的正则表达式
        api.set_regex(True)

        if not api.query():
            error_code = api.get_last_error()
            print(f"搜索失败，错误代码: {error_code}")
        else:
            print("搜索成功")

    except Exception as e:
        print(f"发生异常: {e}")


if __name__ == "__main__":
    # 运行所有示例
    examples = [
        basic_search_example,
        advanced_filter_example,
        media_search_example,
        direct_api_example,
        system_info_example,
        run_history_example,
        error_handling_example,
    ]

    for example in examples:
        try:
            example()
            print("-" * 50)
        except Exception as e:
            print(f"示例 {example.__name__} 执行失败: {e}")
            print("-" * 50)

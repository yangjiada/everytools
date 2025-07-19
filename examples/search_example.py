#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
everytools新API使用示例
Examples for using the new everytools API
"""

from everytools import (
    Search,
    SearchBuilder,
    FileFilter,
    MediaFilter,
    SortType,
    RequestFlag,
)


def simple_search_example():
    """简单搜索示例 - 使用Search类 (高性能)"""
    print("\n=== 简单搜索示例 (Search类) ===")

    try:
        # 最简单的搜索
        search = Search("Python")
        search.execute()
        results = search.get_results()

        print(f"找到 {len(results)} 个结果")
        for i, result in enumerate(results[:5], 1):  # 只显示前5个
            print(f"{i}. {result.name} - {result.full_path}")

        print("\n--- 带参数的搜索 ---")

        # 带参数的搜索
        search = Search(
            query_string="*.py",
            match_case=False,
            sort_type=SortType.SIZE_DESCENDING,
            max_results=10,
            request_flags=RequestFlag.FILE_NAME | RequestFlag.PATH | RequestFlag.SIZE,
        )
        search.execute()
        results = search.get_results()

        print(f"找到 {len(results)} 个Python文件:")
        for result in results:
            size_kb = result.size / 1024 if result.size else 0
            print(f"  {result.name} ({size_kb:.2f} KB)")

    except Exception as e:
        print(f"搜索过程出错: {e}")


def basic_search_example():
    """基本搜索示例"""
    print("\n=== 基本搜索示例 ===")

    try:
        # 创建搜索构建器
        search = (
            SearchBuilder()
            .keywords("Python")  # 搜索关键词
            .match_case(False)  # 不区分大小写
            .limit(10)  # 限制结果数量
            .execute()  # 执行搜索
        )

        # 获取结果
        results = search.get_results()

        # 显示结果数量
        print(f"找到 {len(results)} 个结果(共 {results.total_results} 个)")

        # 遍历结果
        for i, result in enumerate(results, 1):
            try:
                print(f"{i}. {result.full_path} ({result.size} 字节)")
            except Exception as e:
                print(f"处理结果 {i} 时出错: {e}")
    except Exception as e:
        print(f"搜索过程出错: {e}")


def file_filter_example():
    """文件过滤器示例"""
    print("\n=== 文件过滤器示例 ===")

    # 创建文件过滤器
    file_filter = (
        FileFilter().with_extensions("py", "txt").with_size_range(min_size=1024)
    )

    # 使用过滤器搜索
    search = (
        SearchBuilder()
        .keywords("example")
        .filter(file_filter)
        .sort_by(SortType.SIZE_DESCENDING)  # 按大小降序排序
        .execute()
    )

    # 获取结果
    results = search.get_results()

    # 显示结果
    print(f"找到 {len(results)} 个结果")
    for result in results:
        size_kb = result.size / 1024 if result.size else 0
        print(f"{result.name} ({size_kb:.2f} KB)")


def media_filter_example():
    """媒体过滤器示例"""
    print("\n=== 媒体过滤器示例 ===")

    # 创建媒体过滤器
    image_filter = MediaFilter("image")

    # 搜索最近修改的10张图片
    search = (
        SearchBuilder()
        .filter(image_filter)
        .sort_by(SortType.DATE_MODIFIED_DESCENDING)
        .limit(10)
        .execute()
    )

    # 获取结果
    results = search.get_results()

    # 显示结果
    print(f"找到最近修改的 {len(results)} 张图片")
    for result in results:
        print(f"{result.name} - {result.date_modified}")


def async_search_example():
    """异步搜索示例"""
    print("\n=== 异步搜索示例 ===")

    # 创建一个异步搜索
    search = (
        SearchBuilder()
        .keywords("large file")
        .filter(
            FileFilter().with_size_range(min_size=1024 * 1024 * 100)
        )  # 大于100MB的文件
        .execute(async_query=True)  # 异步执行
    )

    print("异步搜索已启动...")

    # 等待搜索完成
    if search.wait_for_completion(timeout_ms=5000):
        print("搜索完成！")
        results = search.get_results()
        print(f"找到 {len(results)} 个大文件")
        for result in results:
            size_mb = result.size / (1024 * 1024) if result.size else 0
            print(f"{result.name} ({size_mb:.2f} MB)")
    else:
        print("搜索超时！")


if __name__ == "__main__":
    simple_search_example()  # 新增：简单搜索示例
    basic_search_example()
    file_filter_example()
    media_filter_example()
    async_search_example()

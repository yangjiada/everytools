#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EveryTools模块搜索示例脚本
演示everytools模块的各种搜索功能和API使用方法
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from everytools import EveryTools
from everytools.constants import SortType

# 尝试导入高级功能（如果可用）
try:
    from everytools import SearchBuilder

    SEARCH_BUILDER_AVAILABLE = True
except ImportError:
    SEARCH_BUILDER_AVAILABLE = False
    print("注意: SearchBuilder功能不可用，将使用基础搜索功能")


def basic_search_examples():
    """基础搜索示例"""
    print("=" * 60)
    print("基础搜索示例")
    print("=" * 60)

    # 创建EveryTools实例
    et = EveryTools()

    # 1. 简单关键词搜索
    print("\n1. 搜索包含'python'的文件和文件夹:")
    et.search("python")
    print(f"找到 {et.get_num_total_results()} 个结果")
    print(f"文件: {et.get_num_total_file()} 个")
    print(f"文件夹: {et.get_num_total_folder()} 个")

    # 显示前5个结果
    results = et.results(max_num=5)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['name']} - {result['path']}")

    # 2. 区分大小写搜索
    print("\n2. 区分大小写搜索'Python':")
    et.search("Python", math_case=True)
    print(f"找到 {et.get_num_total_results()} 个结果")

    # 3. 正则表达式搜索
    print("\n3. 使用正则表达式搜索以'test'开头的文件:")
    et.search("^test", regex=True)
    print(f"找到 {et.get_num_total_results()} 个结果")

    # 显示前3个结果
    results = et.results(max_num=3)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['name']} - {result['path']}")


def file_type_search_examples():
    """文件类型搜索示例"""
    print("\n" + "=" * 60)
    print("文件类型搜索示例")
    print("=" * 60)

    et = EveryTools()

    # 1. 搜索Python文件
    print("\n1. 搜索Python文件:")
    et.search_ext("py", "test")
    print(f"找到 {et.get_num_total_results()} 个Python测试文件")

    results = et.results(max_num=3)
    for i, result in enumerate(results, 1):
        size_mb = result["size"] / (1024 * 1024) if result["size"] > 0 else 0
        print(f"{i}. {result['name']} ({size_mb:.2f} MB)")

    # 2. 搜索图片文件
    print("\n2. 搜索图片文件:")
    et.search_pic("logo")
    print(f"找到 {et.get_num_total_results()} 个包含'logo'的图片")

    # 3. 搜索文档文件
    print("\n3. 搜索文档文件:")
    et.search_doc("readme")
    print(f"找到 {et.get_num_total_results()} 个包含'readme'的文档")

    # 4. 搜索可执行文件
    print("\n4. 搜索可执行文件:")
    et.search_exe("setup")
    print(f"找到 {et.get_num_total_results()} 个包含'setup'的可执行文件")


def advanced_search_examples():
    """高级搜索示例"""
    print("\n" + "=" * 60)
    print("高级搜索示例")
    print("=" * 60)

    et = EveryTools()

    # 1. 在特定路径下搜索
    print("\n1. 在当前项目目录下搜索Python文件:")
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    et.search_in_located(current_dir, "*.py")
    print(f"找到 {et.get_num_total_results()} 个Python文件")

    # 2. 搜索空文件夹
    print("\n2. 搜索文件夹:")
    et.search_folder("test")
    print(f"找到 {et.get_num_total_results()} 个包含'test'的文件夹")

    # 3. 组合搜索条件
    print("\n3. 搜索大于1MB的Python文件:")
    et.search("ext:py size:>1MB")
    print(f"找到 {et.get_num_total_results()} 个大于1MB的Python文件")

    results = et.results(max_num=3, sort_type=SortType.SIZE_DESCENDING.value)
    for i, result in enumerate(results, 1):
        size_mb = result["size"] / (1024 * 1024) if result["size"] > 0 else 0
        print(f"{i}. {result['name']} ({size_mb:.2f} MB) - {result['path']}")


def search_builder_examples():
    """SearchBuilder高级搜索示例"""
    print("\n" + "=" * 60)
    print("SearchBuilder高级搜索示例")
    print("=" * 60)

    try:
        # 1. 链式调用搜索
        print("\n1. 使用SearchBuilder进行链式搜索:")
        search = (
            SearchBuilder()
            .keywords("config")
            .match_case(False)
            .sort_by(SortType.NAME_ASCENDING)
            .limit(5)
            .execute()
        )

        results = search.get_results()
        print(f"找到 {len(results)} 个结果:")

        for i, result in enumerate(results, 1):
            print(f"{i}. {result.name} - {result.full_path}")
            print(f"   大小: {result.size} 字节")
            print(f"   修改时间: {result.date_modified}")

        # 2. 异步搜索
        print("\n2. 异步搜索示例:")
        async_search = (
            SearchBuilder().keywords("python").limit(10).execute(async_query=True)
        )

        if async_search.wait_for_completion(timeout_ms=5000):
            async_results = async_search.get_results()
            print(f"异步搜索完成，找到 {len(async_results)} 个结果")
        else:
            print("异步搜索超时")

    except Exception as e:
        print(f"SearchBuilder示例执行出错: {e}")
        print("可能是因为某些模块尚未完全实现，使用基础搜索功能")


def practical_examples():
    """实用搜索示例"""
    print("\n" + "=" * 60)
    print("实用搜索示例")
    print("=" * 60)

    et = EveryTools()

    # 1. 查找重复文件名
    print("\n1. 查找可能的重复文件:")
    et.search("copy")
    duplicate_candidates = et.results(max_num=5)
    print("可能的重复文件:")
    for i, result in enumerate(duplicate_candidates, 1):
        print(f"{i}. {result['name']} - {result['path']}")

    # 2. 查找大文件
    print("\n2. 查找大于100MB的文件:")
    et.search("size:>100MB")
    large_files = et.results(max_num=5, sort_type=SortType.SIZE_DESCENDING.value)
    print("大文件列表:")
    for i, result in enumerate(large_files, 1):
        size_mb = result["size"] / (1024 * 1024) if result["size"] > 0 else 0
        print(f"{i}. {result['name']} ({size_mb:.2f} MB)")

    # 3. 查找最近修改的文件
    print("\n3. 查找最近修改的Python文件:")
    et.search("ext:py dm:today")
    recent_files = et.results(
        max_num=5, sort_type=SortType.DATE_MODIFIED_DESCENDING.value
    )
    print("最近修改的Python文件:")
    for i, result in enumerate(recent_files, 1):
        print(f"{i}. {result['name']} - {result['modified_date']}")

    # 4. 查找空文件
    print("\n4. 查找空文件:")
    et.search("size:0")
    empty_files = et.results(max_num=5)
    print("空文件列表:")
    for i, result in enumerate(empty_files, 1):
        if result["is_file"]:
            print(f"{i}. {result['name']} - {result['path']}")


def search_statistics():
    """搜索统计信息示例"""
    print("\n" + "=" * 60)
    print("搜索统计信息")
    print("=" * 60)

    et = EveryTools()

    # 统计不同类型文件的数量
    file_types = {
        "Python文件": "ext:py",
        "JavaScript文件": "ext:js",
        "文档文件": "ext:txt;md;doc;docx;pdf",
        "图片文件": "ext:jpg;png;gif;bmp",
        "压缩文件": "ext:zip;rar;7z",
    }

    print("\n文件类型统计:")
    for file_type, query in file_types.items():
        et.search(query)
        count = et.get_num_total_results()
        print(f"{file_type}: {count} 个")

    # 版本信息
    print(f"\nEverything版本: {et.version}")
    print(f"数据库已加载: {et.is_db_loaded()}")
    print(f"管理员权限: {et.is_admin()}")


def main():
    """主函数"""
    print("EveryTools模块搜索示例")
    print("作者: Jan Yang")
    print("时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        # 运行各种示例
        basic_search_examples()
        file_type_search_examples()
        advanced_search_examples()
        search_builder_examples()
        practical_examples()
        search_statistics()

    except Exception as e:
        print(f"\n执行过程中出现错误: {e}")
        print("请确保Everything程序正在运行")

    print("\n" + "=" * 60)
    print("示例执行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

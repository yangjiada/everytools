#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
调试脚本 - 检查文件大小和日期问题
"""

import sys
import os

sys.path.insert(0, ".")

from everytools import EveryTools


def test_basic_search():
    """测试基础搜索功能"""
    print("测试基础搜索功能...")

    et = EveryTools()
    et.search("*.py")

    print(f"找到 {et.get_num_total_results()} 个结果")

    results = list(et.results(max_num=3))

    for i, result in enumerate(results):
        print(f"\n结果 {i+1}:")
        print(f"  文件名: {result['name']}")
        print(f"  路径: {result['path']}")
        print(f"  大小: {result['size']}")
        print(f"  创建日期: {result['created_date']}")
        print(f"  修改日期: {result['modified_date']}")
        print(f"  是否为文件: {result['is_file']}")
        print(f"  是否为文件夹: {result['is_folder']}")


def test_search_builder():
    """测试SearchBuilder功能"""
    print("\n\n测试SearchBuilder功能...")

    try:
        from everytools.query.search import SearchBuilder

        search = SearchBuilder().keywords("*.py").limit(3).execute()
        results = search.get_results()

        print(f"找到 {len(results)} 个结果")

        for i, result in enumerate(results):
            print(f"\n结果 {i+1}:")
            print(f"  文件名: {result.name}")
            print(f"  路径: {result.path}")
            print(f"  完整路径: {result.full_path}")
            print(f"  大小: {result.size}")
            print(f"  创建日期: {result.date_created}")
            print(f"  修改日期: {result.date_modified}")
            print(f"  是否为文件: {result.is_file}")
            print(f"  是否为文件夹: {result.is_folder}")

    except Exception as e:
        print(f"SearchBuilder测试失败: {e}")
        import traceback

        traceback.print_exc()


# 更新主函数调用
if __name__ == "__main__":
    test_basic_search()
    test_search_builder()

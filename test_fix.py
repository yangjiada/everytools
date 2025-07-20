#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试修复后的Search类
"""

import sys

sys.path.insert(0, ".")

from everytools.query.search import SearchBuilder, Search
from everytools.constants import RequestFlag


def test_with_minimal_flags():
    """测试只包含基本标志位的情况"""
    print("测试只包含基本标志位的情况...")

    # 创建只包含基本信息的搜索
    search = Search(
        query_string="*.py", request_flags=RequestFlag.FILE_NAME | RequestFlag.PATH
    )
    search.execute()
    results = search.get_results()

    print(f"找到 {len(results)} 个结果（限制3个）")

    for i, result in enumerate(list(results)[:3]):
        print(f"\n结果 {i+1}:")
        print(f"  文件名: {result.name}")
        print(f"  路径: {result.path}")
        print(f"  大小: {result.size}")  # 应该为None
        print(f"  创建日期: {result.date_created}")  # 应该为None
        print(f"  修改日期: {result.date_modified}")  # 应该为None


def test_with_full_flags():
    """测试包含完整标志位的情况"""
    print("\n\n测试包含完整标志位的情况...")

    # 使用SearchBuilder（应该包含完整标志位）
    search = SearchBuilder().keywords("*.py").limit(3).execute()
    results = search.get_results()

    print(f"找到 {len(results)} 个结果")

    for i, result in enumerate(results):
        print(f"\n结果 {i+1}:")
        print(f"  文件名: {result.name}")
        print(f"  路径: {result.path}")
        print(f"  大小: {result.size}")  # 应该有值
        print(f"  创建日期: {result.date_created}")  # 应该有值
        print(f"  修改日期: {result.date_modified}")  # 应该有值


def test_default_search():
    """测试默认Search构造函数（修复后）"""
    print("\n\n测试默认Search构造函数（修复后）...")

    # 使用默认参数创建Search
    search = Search(query_string="*.py")
    search.execute()
    results = search.get_results()

    print(f"找到 {len(results)} 个结果（限制3个）")

    for i, result in enumerate(list(results)[:3]):
        print(f"\n结果 {i+1}:")
        print(f"  文件名: {result.name}")
        print(f"  路径: {result.path}")
        print(f"  大小: {result.size}")  # 修复后应该有值
        print(f"  创建日期: {result.date_created}")  # 修复后应该有值
        print(f"  修改日期: {result.date_modified}")  # 修复后应该有值


if __name__ == "__main__":
    test_with_minimal_flags()
    test_with_full_flags()
    test_default_search()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EveryTools快速入门示例
简单易懂的搜索示例，适合初学者
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from everytools import EveryTools


def demo_basic_search():
    """基础搜索演示"""
    print("🔍 基础搜索演示")
    print("-" * 40)

    # 创建搜索实例
    et = EveryTools()

    # 搜索包含"python"的文件
    et.search("python")

    print(f"搜索关键词: {et.get_search_keyword()}")
    print(f"总结果数: {et.get_num_total_results()}")
    print(f"文件数: {et.get_num_total_file()}")
    print(f"文件夹数: {et.get_num_total_folder()}")

    # 显示前5个结果
    print("\n前5个搜索结果:")
    for i, result in enumerate(et.results(max_num=5), 1):
        print(f"{i}. {result['name']}")
        print(f"   路径: {result['path']}")
        print(f"   大小: {result['size']} 字节")
        print()


def demo_file_type_search():
    """文件类型搜索演示"""
    print("📁 文件类型搜索演示")
    print("-" * 40)

    et = EveryTools()

    # 搜索Python文件
    print("搜索Python文件:")
    et.search_ext("py")
    print(f"找到 {et.get_num_total_results()} 个Python文件")

    # 搜索图片文件
    print("\n搜索图片文件:")
    et.search_pic()
    print(f"找到 {et.get_num_total_results()} 个图片文件")

    # 搜索文档文件
    print("\n搜索文档文件:")
    et.search_doc()
    print(f"找到 {et.get_num_total_results()} 个文档文件")


def demo_advanced_search():
    """高级搜索演示"""
    print("⚡ 高级搜索演示")
    print("-" * 40)

    et = EveryTools()

    # 在特定目录搜索
    print("在当前项目目录搜索:")
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    et.search_in_located(current_dir, "test")
    print(f"找到 {et.get_num_total_results()} 个包含'test'的文件")

    # 搜索大文件
    print("\n搜索大于1MB的文件:")
    et.search("size:>1MB")
    print(f"找到 {et.get_num_total_results()} 个大文件")

    # 显示前3个大文件
    print("\n最大的3个文件:")
    from everytools.constants import SortType

    for i, result in enumerate(
        et.results(max_num=3, sort_type=SortType.SIZE_DESCENDING.value), 1
    ):
        size_mb = result["size"] / (1024 * 1024) if result["size"] > 0 else 0
        print(f"{i}. {result['name']} ({size_mb:.2f} MB)")


def demo_practical_usage():
    """实用场景演示"""
    print("💡 实用场景演示")
    print("-" * 40)

    et = EveryTools()

    # 查找配置文件
    print("查找配置文件:")
    et.search("config")
    config_files = list(et.results(max_num=3))
    for i, result in enumerate(config_files, 1):
        print(f"{i}. {result['name']} - {result['path']}")

    # 查找日志文件
    print("\n查找日志文件:")
    et.search("ext:log")
    print(f"找到 {et.get_num_total_results()} 个日志文件")

    # 查找临时文件
    print("\n查找临时文件:")
    et.search("ext:tmp;temp")
    print(f"找到 {et.get_num_total_results()} 个临时文件")


def main():
    """主函数 - 运行所有演示"""
    print("=" * 50)
    print("🚀 EveryTools 快速入门示例")
    print("=" * 50)

    try:
        demo_basic_search()
        print("\n")

        demo_file_type_search()
        print("\n")

        demo_advanced_search()
        print("\n")

        demo_practical_usage()

        print("\n" + "=" * 50)
        print("✅ 所有示例运行完成!")
        print("💡 提示: 确保Everything程序正在运行")
        print("=" * 50)

    except Exception as e:
        print(f"❌ 运行出错: {e}")
        print("请确保Everything程序正在运行并且everytools已正确安装")


if __name__ == "__main__":
    main()

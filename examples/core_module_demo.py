#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EveryTools核心模块功能演示
展示everytools模块的核心搜索功能和API使用方法
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from everytools import EveryTools
from everytools.constants import SortType


class EveryToolsDemo:
    """EveryTools演示类"""

    def __init__(self):
        """初始化演示"""
        self.et = EveryTools()
        print(f"EveryTools版本: {self.et.version}")
        print(f"数据库状态: {'已加载' if self.et.is_db_loaded() else '未加载'}")
        print(f"管理员权限: {'是' if self.et.is_admin() else '否'}")
        print("-" * 50)

    def demo_basic_search(self):
        """演示基础搜索功能"""
        print("🔍 基础搜索功能演示")
        print("-" * 30)

        # 1. 简单搜索
        keyword = "config"
        self.et.search(keyword)
        print(f"搜索关键词: '{keyword}'")
        print(f"总结果: {self.et.get_num_total_results()}")
        print(f"文件: {self.et.get_num_total_file()}")
        print(f"文件夹: {self.et.get_num_total_folder()}")

        # 显示结果
        print("\n前3个结果:")
        for i, result in enumerate(self.et.results(max_num=3), 1):
            print(f"{i}. {result['name']}")
            print(f"   路径: {result['path']}")
            print(f"   类型: {'文件' if result['is_file'] else '文件夹'}")
            print(f"   大小: {self._format_size(result['size'])}")
            print()

    def demo_search_options(self):
        """演示搜索选项"""
        print("⚙️ 搜索选项演示")
        print("-" * 30)

        keyword = "Test"

        # 1. 普通搜索
        self.et.search(keyword)
        normal_count = self.et.get_num_total_results()

        # 2. 区分大小写搜索
        self.et.search(keyword, math_case=True)
        case_count = self.et.get_num_total_results()

        # 3. 匹配路径搜索
        self.et.search(keyword, math_path=True)
        path_count = self.et.get_num_total_results()

        # 4. 全字匹配搜索
        self.et.search(keyword, whole_world=True)
        whole_count = self.et.get_num_total_results()

        # 5. 正则表达式搜索
        self.et.search("^test.*\\.py$", regex=True)
        regex_count = self.et.get_num_total_results()

        print(f"关键词 '{keyword}' 搜索结果对比:")
        print(f"普通搜索: {normal_count}")
        print(f"区分大小写: {case_count}")
        print(f"匹配路径: {path_count}")
        print(f"全字匹配: {whole_count}")
        print(f"正则表达式 '^test.*\\.py$': {regex_count}")
        print()

    def demo_file_type_search(self):
        """演示文件类型搜索"""
        print("📁 文件类型搜索演示")
        print("-" * 30)

        # 各种文件类型搜索
        searches = [
            ("Python文件", lambda: self.et.search_ext("py")),
            ("图片文件", lambda: self.et.search_pic()),
            ("文档文件", lambda: self.et.search_doc()),
            ("音频文件", lambda: self.et.search_audio()),
            ("视频文件", lambda: self.et.search_video()),
            ("压缩文件", lambda: self.et.search_zip()),
            ("可执行文件", lambda: self.et.search_exe()),
        ]

        for name, search_func in searches:
            search_func()
            count = self.et.get_num_total_results()
            print(f"{name}: {count} 个")
        print()

    def demo_location_search(self):
        """演示位置搜索"""
        print("📍 位置搜索演示")
        print("-" * 30)

        # 在当前项目目录搜索
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(f"在目录 '{current_dir}' 中搜索:")

        self.et.search_in_located(current_dir, "*.py")
        py_files = self.et.get_num_total_results()

        self.et.search_in_located(current_dir, "test")
        test_files = self.et.get_num_total_results()

        print(f"Python文件: {py_files} 个")
        print(f"包含'test'的文件: {test_files} 个")

        # 搜索文件夹
        self.et.search_folder("examples")
        folder_count = self.et.get_num_total_results()
        print(f"名为'examples'的文件夹: {folder_count} 个")
        print()

    def demo_sorting_and_filtering(self):
        """演示排序和过滤"""
        print("🔄 排序和过滤演示")
        print("-" * 30)

        # 搜索Python文件并按不同方式排序
        self.et.search_ext("py")
        total_count = self.et.get_num_total_results()
        print(f"找到 {total_count} 个Python文件")

        # 按名称排序
        print("\n按名称排序的前3个文件:")
        for i, result in enumerate(
            self.et.results(max_num=3, sort_type=SortType.NAME_ASCENDING.value), 1
        ):
            print(f"{i}. {result['name']}")

        # 按大小排序
        print("\n按大小排序的前3个文件:")
        for i, result in enumerate(
            self.et.results(max_num=3, sort_type=SortType.SIZE_DESCENDING.value), 1
        ):
            size = self._format_size(result["size"])
            print(f"{i}. {result['name']} ({size})")

        # 按修改时间排序
        print("\n按修改时间排序的前3个文件:")
        for i, result in enumerate(
            self.et.results(
                max_num=3, sort_type=SortType.DATE_MODIFIED_DESCENDING.value
            ),
            1,
        ):
            print(f"{i}. {result['name']} - {result['modified_date']}")
        print()

    def demo_advanced_queries(self):
        """演示高级查询"""
        print("⚡ 高级查询演示")
        print("-" * 30)

        # 复杂查询示例
        queries = [
            ("大于1MB的文件", "size:>1MB"),
            ("今天修改的文件", "dm:today"),
            ("空文件", "size:0"),
            ("Python测试文件", "ext:py test"),
            ("包含'config'的JSON文件", "ext:json config"),
        ]

        for description, query in queries:
            self.et.search(query)
            count = self.et.get_num_total_results()
            print(f"{description}: {count} 个")

            # 显示第一个结果
            if count > 0:
                result = next(self.et.results(max_num=1))
                print(f"  示例: {result['name']} - {result['path']}")
        print()

    def demo_result_details(self):
        """演示结果详细信息"""
        print("📋 结果详细信息演示")
        print("-" * 30)

        # 搜索一个具体文件
        self.et.search("setup.py")

        print("setup.py文件详细信息:")
        for i, result in enumerate(self.et.results(max_num=2), 1):
            print(f"\n文件 {i}:")
            print(f"  名称: {result['name']}")
            print(f"  路径: {result['path']}")
            print(f"  完整路径: {os.path.join(result['path'], result['name'])}")
            print(f"  大小: {self._format_size(result['size'])}")
            print(f"  扩展名: {result['file_extension']}")
            print(f"  创建时间: {result['created_date']}")
            print(f"  修改时间: {result['modified_date']}")
            print(f"  是文件: {bool(result['is_file'])}")
            print(f"  是文件夹: {bool(result['is_folder'])}")
            print(f"  是卷: {bool(result['is_volume'])}")
        print()

    def demo_error_handling(self):
        """演示错误处理"""
        print("⚠️ 错误处理演示")
        print("-" * 30)

        # 检查最后错误
        error_code = self.et.get_last_error()
        print(f"最后错误代码: {error_code}")

        # 检查数据库状态
        if not self.et.is_db_loaded():
            print("警告: Everything数据库未加载")
        else:
            print("数据库状态正常")

        print()

    def _format_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        size = float(size_bytes)

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.1f} {units[unit_index]}"

    def run_all_demos(self):
        """运行所有演示"""
        print("=" * 60)
        print("🚀 EveryTools核心模块功能演示")
        print("=" * 60)
        print()

        demos = [
            self.demo_basic_search,
            self.demo_search_options,
            self.demo_file_type_search,
            self.demo_location_search,
            self.demo_sorting_and_filtering,
            self.demo_advanced_queries,
            self.demo_result_details,
            self.demo_error_handling,
        ]

        for demo in demos:
            try:
                demo()
            except Exception as e:
                print(f"演示执行出错: {e}")
                print()

        print("=" * 60)
        print("✅ 所有演示完成!")
        print("💡 提示: 确保Everything程序正在运行以获得最佳效果")
        print("=" * 60)


def main():
    """主函数"""
    try:
        demo = EveryToolsDemo()
        demo.run_all_demos()
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        print("请确保Everything程序正在运行并且everytools已正确安装")


if __name__ == "__main__":
    main()

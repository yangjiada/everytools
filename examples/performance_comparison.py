#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
性能对比示例
Performance comparison between Search and SearchBuilder
"""

import time
from everytools import Search, SearchBuilder, SortType, RequestFlag


def benchmark_search_methods():
    """对比Search和SearchBuilder的性能"""
    print("=== 性能对比测试 ===\n")

    # 测试参数
    test_queries = ["python", "*.txt", "document", "video", "*.pdf"]
    iterations = 10

    print(f"测试查询: {test_queries}")
    print(f"每个查询重复次数: {iterations}")
    print("-" * 50)

    # 测试Search类
    print("🚀 测试Search类 (直接搜索)")
    search_times = []

    for query in test_queries:
        start_time = time.time()

        for _ in range(iterations):
            search = Search(
                query_string=query, max_results=50, sort_type=SortType.NAME_ASCENDING
            )
            search.execute()
            results = search.get_results()

        end_time = time.time()
        avg_time = (end_time - start_time) / iterations
        search_times.append(avg_time)

        print(f"  查询 '{query}': {avg_time*1000:.2f}ms (平均)")

    print()

    # 测试SearchBuilder类
    print("🎨 测试SearchBuilder类 (构建器模式)")
    builder_times = []

    for query in test_queries:
        start_time = time.time()

        for _ in range(iterations):
            search = (
                SearchBuilder()
                .keywords(query)
                .limit(50)
                .sort_by(SortType.NAME_ASCENDING)
                .execute()
            )
            results = search.get_results()

        end_time = time.time()
        avg_time = (end_time - start_time) / iterations
        builder_times.append(avg_time)

        print(f"  查询 '{query}': {avg_time*1000:.2f}ms (平均)")

    print()

    # 性能对比分析
    print("📊 性能对比分析")
    print("-" * 50)

    total_search_time = sum(search_times)
    total_builder_time = sum(builder_times)

    print(f"Search类总耗时: {total_search_time*1000:.2f}ms")
    print(f"SearchBuilder类总耗时: {total_builder_time*1000:.2f}ms")
    print(
        f"性能差异: SearchBuilder比Search慢 {((total_builder_time/total_search_time-1)*100):.1f}%"
    )

    print("\n详细对比:")
    for i, query in enumerate(test_queries):
        search_time = search_times[i] * 1000
        builder_time = builder_times[i] * 1000
        diff_percent = (builder_times[i] / search_times[i] - 1) * 100

        print(f"  '{query}':")
        print(f"    Search: {search_time:.2f}ms")
        print(f"    SearchBuilder: {builder_time:.2f}ms")
        print(f"    差异: +{diff_percent:.1f}%")


def demonstrate_use_cases():
    """演示不同使用场景的最佳选择"""
    print("\n=== 使用场景演示 ===\n")

    # 场景1: 高频简单搜索 - 推荐Search
    print("🔥 场景1: 高频简单搜索 (推荐Search类)")
    print("适用于: 实时搜索、自动补全、批量处理")

    def quick_search_function(keyword):
        """快速搜索函数"""
        search = Search(keyword, max_results=10)
        search.execute()
        return search.get_results()

    # 模拟高频搜索
    keywords = ["py", "pyt", "pyth", "pytho", "python"]
    start_time = time.time()

    for keyword in keywords:
        results = quick_search_function(keyword)
        print(f"  搜索 '{keyword}': 找到 {len(results)} 个结果")

    end_time = time.time()
    print(f"  总耗时: {(end_time-start_time)*1000:.2f}ms")

    print()

    # 场景2: 复杂查询构建 - 推荐SearchBuilder
    print("🎯 场景2: 复杂查询构建 (推荐SearchBuilder类)")
    print("适用于: 多条件过滤、一次性复杂查询、代码可读性要求高")

    from everytools import FileFilter, DateFilter

    start_time = time.time()

    # 复杂查询示例
    complex_results = (
        SearchBuilder()
        .keywords("project")
        .filter(FileFilter().with_extensions("py", "js", "html"))
        .filter(DateFilter().modified_after("2024-01-01"))
        .sort_by(SortType.DATE_MODIFIED_DESCENDING)
        .limit(20)
        .execute()
        .get_results()
    )

    end_time = time.time()
    print(f"  复杂查询结果: 找到 {len(complex_results)} 个文件")
    print(f"  耗时: {(end_time-start_time)*1000:.2f}ms")
    print("  优势: 代码清晰、易于维护、功能丰富")


def memory_usage_comparison():
    """内存使用对比"""
    print("\n=== 内存使用对比 ===\n")

    import sys

    # 测试Search对象大小
    search_obj = Search("test")
    search_size = sys.getsizeof(search_obj)

    # 测试SearchBuilder对象大小
    builder_obj = SearchBuilder().keywords("test")
    builder_size = sys.getsizeof(builder_obj)

    print(f"Search对象大小: {search_size} bytes")
    print(f"SearchBuilder对象大小: {builder_size} bytes")
    print(f"内存差异: SearchBuilder比Search多用 {builder_size-search_size} bytes")

    # 批量创建对象测试
    print("\n批量创建1000个对象:")

    # Search对象
    start_time = time.time()
    search_objects = [Search(f"test{i}") for i in range(1000)]
    search_creation_time = time.time() - start_time

    # SearchBuilder对象
    start_time = time.time()
    builder_objects = [SearchBuilder().keywords(f"test{i}") for i in range(1000)]
    builder_creation_time = time.time() - start_time

    print(f"创建1000个Search对象: {search_creation_time*1000:.2f}ms")
    print(f"创建1000个SearchBuilder对象: {builder_creation_time*1000:.2f}ms")
    print(f"创建速度差异: {((builder_creation_time/search_creation_time-1)*100):.1f}%")


def optimization_tips():
    """性能优化技巧演示"""
    print("\n=== 性能优化技巧 ===\n")

    print("💡 技巧1: 复用Search实例")

    # 不推荐的做法
    start_time = time.time()
    for i in range(100):
        search = Search(f"test{i%10}")  # 重复创建对象
        search.execute()
    bad_time = time.time() - start_time

    # 推荐的做法
    start_time = time.time()
    search = Search("")  # 创建一次
    for i in range(100):
        search._query_string = f"test{i%10}"  # 只修改查询字符串
        search.execute()
    good_time = time.time() - start_time

    print(f"  重复创建对象: {bad_time*1000:.2f}ms")
    print(f"  复用对象: {good_time*1000:.2f}ms")
    print(f"  性能提升: {((bad_time/good_time-1)*100):.1f}%")

    print("\n💡 技巧2: 限制结果数量")

    # 不限制结果
    start_time = time.time()
    search = Search("*")  # 可能返回大量结果
    search.execute()
    unlimited_results = search.get_results()
    unlimited_time = time.time() - start_time

    # 限制结果
    start_time = time.time()
    search = Search("*", max_results=100)  # 限制结果数量
    search.execute()
    limited_results = search.get_results()
    limited_time = time.time() - start_time

    print(f"  不限制结果: {len(unlimited_results)} 个结果, {unlimited_time*1000:.2f}ms")
    print(f"  限制100个结果: {len(limited_results)} 个结果, {limited_time*1000:.2f}ms")
    if unlimited_time > 0:
        print(f"  性能提升: {((unlimited_time/limited_time-1)*100):.1f}%")

    print("\n💡 技巧3: 只请求必要的信息")

    # 请求所有信息
    start_time = time.time()
    search = Search(
        "*.txt",
        max_results=50,
        request_flags=(
            RequestFlag.FILE_NAME
            | RequestFlag.PATH
            | RequestFlag.FULL_PATH_AND_FILE_NAME
            | RequestFlag.SIZE
            | RequestFlag.DATE_CREATED
            | RequestFlag.DATE_MODIFIED
            | RequestFlag.DATE_ACCESSED
            | RequestFlag.EXTENSION
            | RequestFlag.ATTRIBUTES
        ),
    )
    search.execute()
    full_results = search.get_results()
    full_time = time.time() - start_time

    # 只请求基本信息
    start_time = time.time()
    search = Search(
        "*.txt", max_results=50, request_flags=RequestFlag.FILE_NAME | RequestFlag.PATH
    )
    search.execute()
    basic_results = search.get_results()
    basic_time = time.time() - start_time

    print(f"  请求全部信息: {full_time*1000:.2f}ms")
    print(f"  只请求基本信息: {basic_time*1000:.2f}ms")
    if full_time > 0:
        print(f"  性能提升: {((full_time/basic_time-1)*100):.1f}%")


if __name__ == "__main__":
    try:
        benchmark_search_methods()
        demonstrate_use_cases()
        memory_usage_comparison()
        optimization_tips()

        print("\n" + "=" * 60)
        print("📋 总结建议:")
        print("✅ 高频搜索、简单查询 → 使用Search类")
        print("✅ 复杂过滤、一次性查询 → 使用SearchBuilder类")
        print("✅ 性能敏感应用 → 复用对象、限制结果、减少请求信息")
        print("✅ 代码可维护性 → SearchBuilder提供更好的可读性")

    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        print("请确保Everything正在运行且everytools已正确安装")

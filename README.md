# everytools

一个强大的Python库，用于调用Windows系统上的Everything搜索引擎进行高效文件搜索。

## 特性

- 🚀 **高性能搜索** - 基于Everything搜索引擎，毫秒级搜索速度
- 🎯 **现代化API** - 提供链式调用的SearchBuilder和丰富的过滤器
- 🔄 **向后兼容** - 保留传统API，无缝升级
- 🎨 **丰富过滤器** - 支持文件类型、大小、日期、媒体类型等多种过滤
- 📊 **详细结果** - 获取文件名、路径、大小、创建/修改时间等完整信息
- ⚡ **异步支持** - 支持异步搜索，避免阻塞
- 🛡️ **错误处理** - 完善的异常处理机制
- 📝 **完整文档** - 详细的使用说明和示例代码

## 库的整体结构
```
everytools/
├── __init__.py           # 包入口点，导出主要类和函数
├── everytools.py         # 传统API实现（向后兼容）
├── constants.py          # 常量定义（排序类型、请求标志、错误码等）
├── exceptions.py         # 自定义异常类
├── config.py             # 配置管理
├── utils/                # 工具函数模块
│   ├── __init__.py
│   ├── download.py       # Everything SDK DLL下载工具
│   └── time_utils.py     # Windows FILETIME时间转换工具
├── core/                 # 核心功能模块
│   ├── __init__.py
│   ├── dll_loader.py     # DLL加载和初始化管理
│   └── result.py         # 搜索结果处理和封装
├── query/                # 查询功能模块
│   ├── __init__.py
│   ├── search.py         # 现代化搜索API（SearchBuilder）
│   └── filters.py        # 搜索过滤器（文件、日期、媒体等）
└── dll/                  # Everything SDK DLL文件存放目录
    ├── Everything32.dll  # 32位DLL（自动下载）
    └── Everything64.dll  # 64位DLL（自动下载）
```

## 运行环境

### 安装everything软件

由于需要调用电脑版everything程序，没有安装的需要[下载](https://www.voidtools.com/zh-cn/downloads/)安装everything，安装完后请确保已经运行，任务栏会出现程序图标。

### 安装everytools库

在命令行窗口下使用pip进行安装everytools库

```shell
pip install everytools
```

## 使用方法

### 新API (推荐)

从v0.2.0开始，everytools提供了更加现代化、易用的API。根据不同的使用场景，我们提供了两种搜索方式：

#### 1. 简单搜索 - Search类 (高性能)

适用于简单查询和性能敏感的场景：

```python
from everytools import Search

# 直接创建搜索实例
search = Search("Python")
search.execute()
results = search.get_results()

# 遍历结果
for result in results:
    print(f"{result.name} - {result.full_path} ({result.size} bytes)")
```

带参数的简单搜索：

```python
from everytools import Search, SortType, RequestFlag

# 创建带参数的搜索
search = Search(
    query_string="*.py",
    match_case=False,
    sort_type=SortType.SIZE_DESCENDING,
    max_results=10,
    request_flags=RequestFlag.FILE_NAME | RequestFlag.PATH | RequestFlag.SIZE
)
search.execute()
results = search.get_results()
```

#### 2. 构建器搜索 - SearchBuilder类 (易用性)

适用于复杂查询构建和需要链式调用的场景：

```python
from everytools import SearchBuilder, FileFilter, SortType

# 创建搜索构建器
search = (
    SearchBuilder()
    .keywords("Python")  # 搜索关键词
    .filter(FileFilter().with_extensions("py", "txt"))  # 过滤器
    .match_case(False)   # 不区分大小写
    .sort_by(SortType.SIZE_DESCENDING)  # 按大小降序排序
    .limit(10)           # 限制结果数量
    .execute()           # 执行搜索
)

# 获取结果
results = search.get_results()

# 遍历结果
for result in results:
    print(f"{result.name} - {result.full_path} ({result.size} bytes)")
```

#### 性能对比与使用建议

**Search类 vs SearchBuilder类的性能差异：**

| 特性 | Search类 | SearchBuilder类 |
|------|----------|----------------|
| 执行速度 | ⚡ 更快 | 🐌 较慢 |
| 内存占用 | 💾 更少 | 📦 较多 |
| 代码简洁性 | 📝 简单直接 | 🎨 链式调用 |
| 功能丰富性 | 🔧 基础功能 | 🛠️ 丰富过滤器 |

**性能差异原因：**
- SearchBuilder需要额外的对象创建和参数传递开销
- SearchBuilder在execute()时会创建新的Search实例
- 查询字符串需要动态构建和组装

**使用场景建议：**

```python
# ✅ 推荐使用Search类的场景：
# 1. 高频查询（如实时搜索）
# 2. 简单关键词搜索
# 3. 性能敏感的应用
# 4. 批量处理大量搜索请求

from everytools import Search

# 高频搜索示例
def quick_search(keyword):
    search = Search(keyword)
    search.execute()
    return search.get_results()

# ✅ 推荐使用SearchBuilder类的场景：
# 1. 复杂查询条件组合
# 2. 需要多种过滤器
# 3. 代码可读性要求高
# 4. 一次性查询任务

from everytools import SearchBuilder, FileFilter, DateFilter

# 复杂查询示例
def complex_search():
    return (
        SearchBuilder()
        .keywords("project")
        .filter(FileFilter().with_extensions("py", "js"))
        .filter(DateFilter().modified_after("2024-01-01"))
        .sort_by(SortType.DATE_MODIFIED_DESCENDING)
        .limit(50)
        .execute()
        .get_results()
    )
```

**性能优化技巧：**

```python
# 1. 复用Search实例
search = Search("")
for keyword in ["python", "java", "javascript"]:
    search._query_string = keyword
    search.execute()
    results = search.get_results()
    # 处理结果...

# 2. 预设常用搜索配置
def create_optimized_search(query):
    return Search(
        query_string=query,
        max_results=100,  # 限制结果数量
        request_flags=RequestFlag.FILE_NAME | RequestFlag.PATH  # 只请求必要信息
    )

# 3. 批量处理
def batch_search(keywords, batch_size=10):
    results = {}
    for i in range(0, len(keywords), batch_size):
        batch = keywords[i:i+batch_size]
        for keyword in batch:
            search = Search(keyword)
            search.execute()
            results[keyword] = search.get_results()
    return results
```

#### 使用过滤器

everytools提供了丰富的过滤器来精确控制搜索结果：

```python
from everytools import SearchBuilder, FileFilter, FolderFilter, MediaFilter, DocumentFilter, DateFilter, SizeFilter

# 文件过滤器 - 搜索大于1MB的Python文件
python_files = FileFilter().with_extensions("py").with_size_range(min_size=1024*1024)

# 文件夹过滤器 - 搜索空文件夹
empty_folders = FolderFilter().empty_only()

# 媒体过滤器 - 搜索图片文件
images = MediaFilter("image")  # 支持 "audio", "video", "image", "all"

# 文档过滤器 - 搜索Office文档
documents = DocumentFilter("office")  # 支持 "office", "pdf", "text", "all"

# 日期过滤器 - 搜索最近修改的文件
recent_files = DateFilter().modified_after("2024-01-01")

# 大小过滤器 - 搜索大文件
large_files = SizeFilter().larger_than_mb(100)  # 大于100MB

# 组合多个过滤器
search = (
    SearchBuilder()
    .keywords("project")
    .filter(python_files)
    .filter(recent_files)
    .sort_by(SortType.DATE_MODIFIED_DESCENDING)
    .execute()
)
```

##### 过滤器详细说明

**FileFilter（文件过滤器）**
```python
file_filter = (
    FileFilter()
    .with_extensions("py", "txt", "md")  # 指定文件扩展名
    .with_size_range(min_size=1024, max_size=1024*1024)  # 文件大小范围
    .with_content("TODO")  # 搜索文件内容（仅文本文件）
    .duplicates_only()  # 仅显示重复文件
)
```

**DateFilter（日期过滤器）**
```python
date_filter = (
    DateFilter()
    .by_modified_date()  # 按修改日期过滤
    .in_range("2024-01-01", "2024-12-31")  # 日期范围
)

# 便捷方法
recent_created = DateFilter().created_after("2024-06-01")
recent_modified = DateFilter().modified_after("2024-06-01")
```

**SizeFilter（大小过滤器）**
```python
size_filter = (
    SizeFilter()
    .larger_than_mb(10)  # 大于10MB
    .smaller_than_gb(1)  # 小于1GB
)
```

#### 异步搜索

```python
from everytools import SearchBuilder

# 创建一个异步搜索
search = SearchBuilder().keywords("large files").execute(async_query=True)

# 等待搜索完成
if search.wait_for_completion(timeout_ms=5000):
    results = search.get_results()
    print(f"找到 {len(results)} 个结果")
else:
    print("搜索超时！")
```

### 传统API (向后兼容)

为了兼容旧版本，我们继续保留了传统API：

```python
# 导入EveryTools类
from everytools import EveryTools

es = EveryTools()  # 实例化，只需要第一次就行
```

#### 用名称搜索

使用`search()`方法可以通过输入关键词检索文件，一般在几秒内能结束，检索完后可以读取结果数量。

```python
es.search('工作')
print('everything reuslt number:', es.get_num_total_results())  # 获取搜索结果对象数量
```

#### 获取搜索数量

搜索后可以获得的数量有三种：结果总数量、文件数量、文件夹数量。

```python
es.get_num_total_results()  #总数量
es.get_num_total_file()  # 文件数量
es.get_num_total_folder()  # 文件夹数量
```

#### 获取搜索结果

使用`results()`获取搜索结果，该返回为迭代器。输出结果会包含name, path等信息，由于检索信息需要耗一定时间，数量比较多的情况下需要等待片刻。

```python
results = es.results()  # 获取输出结果

# 只打印前五个结果
for i, result in enumerate(results):
    if i >= 5:
        break
    print(result)
```

#### 更改结果排序

更改`results`方法`sort_type`参数实现更改排序结果，默认参数为`1`，其他参数如下：

| **排序类型** | **值** |
| :----------: | :----: |
|   名称升序   |   1    |
|   名称降序   |   2    |
|   路径升序   |   3    |
|   路径降序   |   4    |
|   大小升序   |   5    |
|   大小降序   |   6    |
|  拓展名升序  |   7    |
|  拓展名降序  |   8    |

#### 快速搜索方法

```python
es.search_audio()  # 搜索音频
es.search_zip()  # 搜索压缩包
es.search_doc()  # 搜索文档
es.search_exe()  # 搜索可执行文件
es.search_folder()  # 搜索文件夹
es.search_pic()  # 搜索图片
es.search_video()  # 搜索视频
es.search_ext(ext='pdf')  # 搜索文件拓展
es.search_in_located('C:\\Users\\')  # 搜索指定文件夹下
```

## 高级功能

### 搜索结果详细信息

每个搜索结果包含丰富的文件信息：

```python
from everytools import SearchBuilder

search = SearchBuilder().keywords("example").limit(1).execute()
results = search.get_results()

for result in results:
    print(f"文件名: {result.name}")
    print(f"路径: {result.path}")
    print(f"完整路径: {result.full_path}")
    print(f"文件大小: {result.size} 字节")
    print(f"创建时间: {result.date_created}")
    print(f"修改时间: {result.date_modified}")
    print(f"访问时间: {result.date_accessed}")
    print(f"文件扩展名: {result.extension}")
    print(f"是否为文件: {result.is_file}")
    print(f"是否为文件夹: {result.is_folder}")
    print(f"文件属性: {result.attributes}")
```

### 排序选项

everytools支持多种排序方式：

```python
from everytools import SearchBuilder, SortType

# 按名称排序
search = SearchBuilder().keywords("test").sort_by(SortType.NAME_ASCENDING).execute()

# 按大小排序
search = SearchBuilder().keywords("test").sort_by(SortType.SIZE_DESCENDING).execute()

# 按修改时间排序
search = SearchBuilder().keywords("test").sort_by(SortType.DATE_MODIFIED_DESCENDING).execute()
```

**可用的排序类型：**
- `NAME_ASCENDING` / `NAME_DESCENDING` - 按名称排序
- `PATH_ASCENDING` / `PATH_DESCENDING` - 按路径排序  
- `SIZE_ASCENDING` / `SIZE_DESCENDING` - 按大小排序
- `EXTENSION_ASCENDING` / `EXTENSION_DESCENDING` - 按扩展名排序
- `DATE_CREATED_ASCENDING` / `DATE_CREATED_DESCENDING` - 按创建时间排序
- `DATE_MODIFIED_ASCENDING` / `DATE_MODIFIED_DESCENDING` - 按修改时间排序
- `DATE_ACCESSED_ASCENDING` / `DATE_ACCESSED_DESCENDING` - 按访问时间排序

### 错误处理

everytools提供了完善的错误处理机制：

```python
from everytools import SearchBuilder, EverythingError

try:
    search = SearchBuilder().keywords("test").execute()
    results = search.get_results()
    print(f"找到 {len(results)} 个结果")
except EverythingError as e:
    print(f"搜索出错: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

### 系统信息查询

```python
from everytools.core.dll_loader import get_dll_loader

loader = get_dll_loader()
print(f"Everything版本: {loader.version}")
print(f"数据库已加载: {loader.is_db_loaded()}")
print(f"管理员权限: {loader.is_admin()}")
```

## Everything搜索语法

everytools完全支持Everything的强大搜索语法，可以直接在关键词中使用：

### 基本语法

```python
# 通配符
SearchBuilder().keywords("*.txt").execute()  # 所有txt文件
SearchBuilder().keywords("test?.doc").execute()  # test后跟一个字符的doc文件

# 逻辑操作符
SearchBuilder().keywords("python AND tutorial").execute()  # 包含python和tutorial
SearchBuilder().keywords("python OR java").execute()  # 包含python或java
SearchBuilder().keywords("python NOT tutorial").execute()  # 包含python但不包含tutorial

# 路径搜索
SearchBuilder().keywords("c:\\users\\").execute()  # 在特定路径下搜索
SearchBuilder().keywords("parent:c:\\users\\").execute()  # 父目录为指定路径
```

### 高级语法

```python
# 文件大小
SearchBuilder().keywords("size:>1mb").execute()  # 大于1MB的文件
SearchBuilder().keywords("size:1kb..1mb").execute()  # 1KB到1MB之间的文件

# 日期搜索
SearchBuilder().keywords("dm:today").execute()  # 今天修改的文件
SearchBuilder().keywords("dc:2024").execute()  # 2024年创建的文件
SearchBuilder().keywords("dm:>2024/1/1").execute()  # 2024年1月1日后修改的文件

# 文件属性
SearchBuilder().keywords("attrib:h").execute()  # 隐藏文件
SearchBuilder().keywords("attrib:r").execute()  # 只读文件

# 正则表达式
SearchBuilder().keywords("regex:test\\d+\\.txt").use_regex(True).execute()
```

### 常用搜索模式

```python
# 查找重复文件
SearchBuilder().keywords("dupe:").execute()

# 查找空文件夹
SearchBuilder().keywords("empty:").execute()

# 查找大文件（前100个最大的文件）
SearchBuilder().keywords("").sort_by(SortType.SIZE_DESCENDING).limit(100).execute()

# 查找最近修改的文件
SearchBuilder().keywords("dm:today").sort_by(SortType.DATE_MODIFIED_DESCENDING).execute()
```

## 实用示例

### 常见使用场景

#### 1. 清理重复文件

```python
from everytools import SearchBuilder, FileFilter

# 查找重复文件
duplicates = SearchBuilder().keywords("dupe:").execute().get_results()

print(f"找到 {len(duplicates)} 个重复文件:")
for file in duplicates:
    print(f"- {file.full_path} ({file.size} bytes)")
```

#### 2. 查找大文件释放空间

```python
from everytools import SearchBuilder, SortType

# 查找最大的100个文件
large_files = (
    SearchBuilder()
    .keywords("")  # 搜索所有文件
    .sort_by(SortType.SIZE_DESCENDING)
    .limit(100)
    .execute()
    .get_results()
)

print("最大的文件:")
for file in large_files[:10]:  # 显示前10个
    size_mb = file.size / (1024 * 1024) if file.size else 0
    print(f"- {file.name}: {size_mb:.2f} MB")
```

#### 3. 项目文件管理

```python
from everytools import SearchBuilder, FileFilter, DateFilter

# 查找项目中的Python文件，按最近修改时间排序
project_files = (
    SearchBuilder()
    .keywords("C:\\MyProject\\")  # 指定项目路径
    .filter(FileFilter().with_extensions("py", "js", "html", "css"))
    .filter(DateFilter().modified_after("2024-01-01"))
    .sort_by(SortType.DATE_MODIFIED_DESCENDING)
    .execute()
    .get_results()
)

print("最近修改的项目文件:")
for file in project_files[:20]:
    print(f"- {file.name} (修改于: {file.date_modified})")
```

#### 4. 媒体文件整理

```python
from everytools import SearchBuilder, MediaFilter, SizeFilter

# 查找大于50MB的视频文件
large_videos = (
    SearchBuilder()
    .filter(MediaFilter("video"))
    .filter(SizeFilter().larger_than_mb(50))
    .sort_by(SortType.SIZE_DESCENDING)
    .execute()
    .get_results()
)

print("大视频文件:")
for video in large_videos:
    size_gb = video.size / (1024 * 1024 * 1024) if video.size else 0
    print(f"- {video.name}: {size_gb:.2f} GB")
```

#### 5. 系统清理

```python
from everytools import SearchBuilder, FileFilter

# 查找临时文件
temp_files = (
    SearchBuilder()
    .filter(FileFilter().with_extensions("tmp", "temp", "cache", "log"))
    .filter(DateFilter().modified_after("2024-01-01"))
    .execute()
    .get_results()
)

print(f"找到 {len(temp_files)} 个临时文件")

# 查找空文件夹
empty_folders = SearchBuilder().keywords("empty:").execute().get_results()
print(f"找到 {len(empty_folders)} 个空文件夹")
```

### 性能优化建议

#### 1. 使用适当的过滤器

```python
# 好的做法：使用具体的过滤器
search = (
    SearchBuilder()
    .keywords("report")
    .filter(FileFilter().with_extensions("pdf", "docx"))
    .filter(DateFilter().modified_after("2024-01-01"))
    .limit(100)  # 限制结果数量
    .execute()
)

# 避免：过于宽泛的搜索
# search = SearchBuilder().keywords("").execute()  # 会返回所有文件
```

#### 2. 合理使用限制

```python
# 对于大量结果，使用limit限制
search = SearchBuilder().keywords("*.txt").limit(1000).execute()

# 或者分批处理
def process_search_results(keywords, batch_size=100):
    search = SearchBuilder().keywords(keywords).execute()
    results = search.get_results()
    
    for i in range(0, len(results), batch_size):
        batch = list(results)[i:i+batch_size]
        # 处理这一批结果
        yield batch
```

#### 3. 异步搜索处理

```python
import time
from everytools import SearchBuilder

def search_with_timeout(keywords, timeout_seconds=10):
    search = SearchBuilder().keywords(keywords).execute(async_query=True)
    
    if search.wait_for_completion(timeout_ms=timeout_seconds * 1000):
        return search.get_results()
    else:
        print("搜索超时")
        return []

# 使用示例
results = search_with_timeout("large files", timeout_seconds=5)
```

## 故障排除

### 常见问题

#### 1. Everything未运行

```python
from everytools.core.dll_loader import get_dll_loader

try:
    loader = get_dll_loader()
    if not loader.is_db_loaded():
        print("Everything数据库未加载，请确保Everything正在运行")
except Exception as e:
    print(f"无法连接到Everything: {e}")
    print("请确保：")
    print("1. Everything已安装并正在运行")
    print("2. Everything服务已启动")
    print("3. 当前用户有足够权限")
```

#### 2. DLL加载失败

```python
import os
from everytools.utils.download import download_sdk_dll

# 手动下载DLL
dll_dir = os.path.join(os.path.dirname(__file__), "everytools", "dll")
try:
    download_sdk_dll(dll_dir)
    print("DLL下载成功")
except Exception as e:
    print(f"DLL下载失败: {e}")
```

#### 3. 搜索结果为空

```python
from everytools import SearchBuilder

search = SearchBuilder().keywords("test").execute()
results = search.get_results()

if len(results) == 0:
    print("搜索结果为空，可能的原因：")
    print("1. 搜索关键词不存在")
    print("2. Everything索引未完成")
    print("3. 搜索路径不在索引范围内")
    
    # 尝试更宽泛的搜索
    broad_search = SearchBuilder().keywords("*").limit(10).execute()
    broad_results = broad_search.get_results()
    print(f"宽泛搜索找到 {len(broad_results)} 个结果")
```

## 其他方法

### 查看版本信息

```python
# 新API方式
from everytools.core.dll_loader import get_dll_loader
loader = get_dll_loader()
print(f"Everything版本: {loader.version}")

# 传统API方式
from everytools import EveryTools
es = EveryTools()
print(f"主要版本: {es.major_version}")
print(f"次要版本: {es.minor_version}")
print(f"修正版: {es.revision}")
print(f"编译号: {es.build_number}")
print(f"完整版本: {es.version}")
```

![image](images/1.png)

## 版本更新

| **版本** |                          **更新内容**                          |  **日期**  |
| :------: | :------------------------------------------------------------: | :--------: |
| 0.2.0    | 重构项目架构，提供新的现代API，支持异步搜索和更多过滤功能     | 2025-07-19 |
| 0.0.1.4    | 去掉多余的pandas模块     | 2025-07-06 |
| 0.0.1.2  | 修复搜索拓展不生效，输出结果新增拓展名，优化搜索为空返回值     | 2021-10-06 |
| 0.0.1.1  | 修复安装时环境依赖警告                                         | 2021-09-25 |
| 0.0.1.0  | 提供everything基本搜索以及快速搜索方法。                       | 2021-09-25 |

## 联系作者

**作者(author)：Jan Yang**

**邮箱(Email)：yang.jiada@foxmail.com**


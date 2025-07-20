# EveryTools 示例文件

这个目录包含了EveryTools模块的各种使用示例，帮助你快速上手和掌握搜索功能。

## 文件说明

### 1. `quick_start_examples.py` - 快速入门示例
- **适合人群**: 初学者
- **内容**: 基础搜索功能演示
- **特点**: 简单易懂，快速上手

```bash
python examples/quick_start_examples.py
```

### 2. `core_module_demo.py` - 核心模块功能演示
- **适合人群**: 想深入了解模块功能的用户
- **内容**: 完整的API功能演示
- **特点**: 详细的功能展示和错误处理

```bash
python examples/core_module_demo.py
```

### 3. `module_search_examples.py` - 模块搜索示例
- **适合人群**: 高级用户
- **内容**: 各种搜索场景和高级功能
- **特点**: 实用的搜索技巧和最佳实践

```bash
python examples/module_search_examples.py
```

### 4. `search_example.ipynb` - Jupyter笔记本示例
- **适合人群**: 喜欢交互式学习的用户
- **内容**: 可交互的搜索示例
- **特点**: 可以逐步执行和修改代码

## 使用前准备

1. **确保Everything程序正在运行**
   - 下载并安装 [Everything](https://www.voidtools.com/)
   - 启动Everything程序并等待索引完成

2. **安装everytools模块**
   ```bash
   pip install everytools
   ```
   或者在项目根目录运行:
   ```bash
   pip install -e .
   ```

## 基础用法示例

### 简单搜索
```python
from everytools import EveryTools

# 创建搜索实例
et = EveryTools()

# 搜索包含"python"的文件
et.search("python")

# 获取结果统计
print(f"找到 {et.get_num_total_results()} 个结果")
print(f"文件: {et.get_num_total_file()} 个")
print(f"文件夹: {et.get_num_total_folder()} 个")

# 遍历结果
for result in et.results(max_num=5):
    print(f"{result['name']} - {result['path']}")
```

### 文件类型搜索
```python
# 搜索Python文件
et.search_ext("py")

# 搜索图片文件
et.search_pic("logo")

# 搜索文档文件
et.search_doc("readme")
```

### 高级搜索
```python
# 搜索大于1MB的文件
et.search("size:>1MB")

# 搜索今天修改的文件
et.search("dm:today")

# 在特定目录搜索
et.search_in_located("C:\\Projects", "*.py")
```

## 搜索语法参考

### 基本语法
- `python` - 搜索包含"python"的文件和文件夹
- `*.py` - 搜索所有Python文件
- `folder:` - 只搜索文件夹

### 文件属性
- `ext:py` - 按扩展名搜索
- `size:>1MB` - 按文件大小搜索
- `dm:today` - 按修改日期搜索
- `dc:yesterday` - 按创建日期搜索

### 逻辑操作
- `python AND test` - 同时包含两个关键词
- `python OR java` - 包含任一关键词
- `python !test` - 包含python但不包含test

### 正则表达式
```python
# 启用正则表达式搜索
et.search("^test.*\\.py$", regex=True)
```

## 常见问题

### Q: 搜索结果为空或很少
A: 确保Everything程序正在运行并且已完成文件索引

### Q: 程序报错"找不到DLL"
A: 程序会自动下载所需的DLL文件，请确保网络连接正常

### Q: 搜索速度慢
A: Everything的搜索速度取决于索引状态，首次使用时需要等待索引完成

### Q: 无法搜索网络驱动器
A: 需要在Everything设置中启用网络驱动器索引

## 更多资源

- [Everything官方网站](https://www.voidtools.com/)
- [Everything搜索语法](https://www.voidtools.com/support/everything/searching/)
- [项目GitHub仓库](https://github.com/yangjiada/everytools)

## 贡献

欢迎提交更多示例和改进建议！请通过GitHub Issues或Pull Requests参与贡献。
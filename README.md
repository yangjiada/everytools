# everytools
用Python调用everything进行文件搜索的工具，只适用于Windows系统。

## 运行环境

### 安装everything软件

由于需要调用电脑版everything程序，没有安装的需要[下载](https://www.voidtools.com/zh-cn/downloads/)安装everything，安装完后请确保已经运行，任务栏会出现程序图标。

### 安装everytools库

在命令行窗口下使用pip进行安装everytools库

```shell
pip install everytools
```



## 初始化

everytools是通过EveryTools类来连接everything软件进行搜索（比使用python遍历目录快很多），具体是用everything提供的SDK来实现，`dll`文件夹下面有两个dll文件，`Everything64.dll`适用于64位系统，`Everything32.dll`适用于32位系统，默认是64位系统，如果是32位系统需要更改参数

```python
# 导入EveryTools类
from everytools import EveryTools

es = EveryTools()  # 实例化，只需要第一次就行
```



## 搜索文件

### 用名称搜索

使用`search()`方法可以通过输入关键词检索文件，一般在几秒内能结束，检索完后可以读取结果数量。

```python
es.search('工作')
print('everything reuslt number:', es.get_num_total_results())  # 获取搜索结果对象数量
```

### 获取搜索数量

搜索后可以获得的数量有三种：结果总数量、文件数量、文件夹数量。

```python
es.get_num_total_results()  #总数量
es.get_num_total_file()  # 文件数量
es.get_num_total_folder()  # 文件夹数量
```

### 获取搜索结果

为了方便处理搜索结果输出采用pandas DataFrame进行保存，使用`results()`方法既可以输出结果。输出结果会包含name, path等信息，由于检索信息需要耗一定时间，数量比较多的情况下需要等待片刻。

```python
results = es.results()  # 获取输出结果
print(results)  # 查看前五行数据
```

### 更改结果排序

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



### 快速搜索方法

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



## 搜索语法

evertools支持所有everything语法，通过everything的帮助获得搜索语法，具体有以下功能：

* 操作符
* 通配符
* 宏
* 修饰符
* 函数
* 函数语法
* 大小语法
* 大小常数
* 日期语法
* 日期常数
* 属性常数

## 其他方法

### 查看版本信息

```python
es.major_version  # 主要版本
es.minor_version  # 次要版本
es.revision  # 修正版
es.build_number  # 编译号
es.version  # 版本号
```

![image](images/1.png)

## 版本更新

| **版本** |                        **更新内容**                        |  **日期**  |
| :------: | :--------------------------------------------------------: | :--------: |
| 0.0.1.4  | 去掉多余模块 | 2025-07-06 |
| 0.0.1.2  | 修复搜索拓展不生效，输出结果新增拓展名，优化搜索为空返回值 | 2021-10-06 |
| 0.0.1.1  |                   修复安装时环境依赖警告                   | 2021-09-25 |
| 0.0.1.0  |          提供everything基本搜索以及快速搜索方法。          | 2021-09-25 |

## 联系作者

**作者(author)：Jan Yang**

**邮箱(Email)：yang.jiada@foxmail.com**


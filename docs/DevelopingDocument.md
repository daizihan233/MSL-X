# 欢迎来到MSLX Developing Document

## Chapter 1 目的

### 写这篇文档是为了更加清晰地展示MSLX的结构，以帮助开发

## Chapter 2 文件结构

### 这里展示了MSLX的文件目录结构(截止于Beta 0.06 Preview 3)以及相应说明

- assets 储存MSLX所使用的资源文件

  - fonts 字体文件位于此处
  - icons 图标文件位于此处
- Config 储存MSLX的配置文件

  - \_\_init\_\_.py 是便于程序内部调用而存在的，如果没有发现此文件请手动创建一个(内容请留空)
  - Default.json 程序运行后手动保存的配置文件（未更改名称的情况下）
- Crypt 储存RSA公/密钥（当前未启用）
- docs 储存文档（包括这篇文档在内）
- lib 储存MSLX的一些函数

  - crypt 储存AES和RSA加解密的相关文件
  - create_settings.py 保存和读取配置文件
  - download.py MSLX的下载器（当前未启用）
- ui 储存MSLX的其他页面以及其对应的函数

  - frpconfig.py 内网穿透配置页面和函数（未启用）
  - logs.py 日志页面和函数（未启用）
  - settings.py 软件设置页面和函数（未启用）
- .gitgnore Git提交时的忽略文件列表
- build.cmd Windows下快速使用Pyinstaller打包MSLX
- Custom.py 在主程序初始化时调用的用户附加程序
- LICENSE 许可证
- logo.png 打包时使用的文件logo
- main.py MSLX的主程序，运行即可弹出主窗口
- mslx.spec和mslx_unix.spec 分别在Windows和Unix上使用Pyinstaller打包时可以使用的配置文件
- README.md 展示在项目首页的README
- requirements.txt MSLX的所有运行库依赖列表，可以用来快速进行安装（参见使用文档第一节：下载运行环境）

## Chapter 3 main.py函数说明

### 整个文件的主要部分是main函数

软件的初始化部分分为：

- 定义变量/常量
- 设定页面属性（初始化页面）
- 向页面添加控件
- 刷新页面

#### 定义变量/常量

##### 这部分代码不存放在任何子函数里，直接归属于main函数

- use_java java的路径
- xms和xmx 分别为服务器的最小内存和最大内存
- server_path 服务端所在路径
- server_file 服务端名称(包括后缀)
- server_options 服务端的启动参数
- 将xmx设为当前最大可用内存的70%
- hitokoto 要显示的一言

#### 设定页面属性（初始化页面）

##### 实现这个功能的代码存放在init_page方法里

- 设置窗口标题格式为MSLX | 页面名称
- 设置窗口高650
- 设置窗口宽1250
- 设置窗口的字体

#### 向页面添加控件

##### 实现这个功能的代码存放在create_controls方法里

程序内已在相应位置做了注释，故此处不再展开说明

# 使用前

> 这篇文档的Linux部分除Arch特编外皆以Ubuntu 22.04 LTS为基础
>
> Arch特编部分如无特殊要求皆使用root用户身份执行
>
>> yay和makepkg部分请用普通用户执行(如用root则可能会对系统造成不可挽回的破坏)
>>

## 下载运行环境

### Python

- Linux(命令行安装，请准备好sudo/root权限)
  现在请您先输入python --version查看现存Python版本，3.10以下都不可以运行
- 如果您是Python2.x，请在终端输入sudo apt remove --auto-remove python2.x 来移除Python(把x换成后面的版本号)，然后按照Python3.x-Python3.10以下处理
- 如果您是Python3.x：

  - Python3.10以上可以直接跳到下载运行环境一节
  - Python3.10以下可以查看[教程](https://cloud.tencent.com/developer/article/1565853)或自己折腾
  - Windows/macOS(官网直接下载安装包安装)

    - Windows前往[这里](https://www.python.org/downloads/windows/)
    - macOS前往[这里](https://www.python.org/downloads/macos/)
    - Windows用户下载Windows installer(64-bit)，切记安装时要在下方勾选"Add Python 3.xx.x to Path"
    - macOS用户下载macOS 64-bit universal2 installer

#### Arch特编

##### 您只需要运行以下命令，便可安装Python3.10：

``pacman -S python``

##### 其他

- 恭喜您选择了Arch Linux!
- 由于最新版本的Arch Linux已经停止了Python3.7以前版本的支持，本文不做说明
- 如果您希望使用Python311，请您使用AUR：

  - [Python311 on AUR](https://aur.archlinux.org/packages/python311)
  - [AUR](https://wiki.archlinux.org/title/Arch_User_Repository)
  - [Pacman](https://wiki.archlinuxcn.org/wiki/Pacman)
- 作为一个老练的Arch Linux用户，您应该知道怎么使用
- 使用yay

  - 安装

    - 以root账户执行下列命令：

      ```bash
      pacman -S git go base-devel
      git clone https://aur.archlinux.org/yay.git
      cd yay
      ```

    再切换到一个非root用户来执行makepkg：

    ```bash
    su xxx(用户名)
    makepkg -si
    ```
  - 使用

    - 它的语法和pacman一致。
    - 示例：您可以通过以下语句来安装Python3.11:
      ``yay -S python311``

### 如果您已经配置好了Python3.7(或更高)环境，请在终端执行pip install -r requirements.txt以安装依赖

#### 注：此处请保证终端的路径处于我们的项目文件根目录

#### 注2：如果您正在使用Linux请将pip替换为sudo pip3

### Java

> 虽然开服器本身并不需要Java，可Java是开服的必需品，所以在此一并列出其下载方式（仅针对Linux）

#### 使用apt安装

##### 如您的发行版可以使用apt，请按照您的情况选择命令（必须要有root权限，推荐直接复制）：

- 首先，更新您的下载源:
- ``sudo apt update && sudo apt upgrade -y``
- Java17：``sudo apt install openjdk-17-jdk -y``
- Java16：``sudo apt install openjdk-16-jdk -y``
- Java8：``sudo apt install openjdk-8-jdk -y``
- Java7：``sudo apt install openjdk-7-jdk -y``

#### 手动下载安装包

##### 如果您的发行版使用不了apt或者上面的命令报错，请尝试在这里下载：

- [Java17下载](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
- [Java16下载](https://www.oracle.com/java/technologies/javase/jdk16-archive-downloads.html)
- [Java8下载](https://www.oracle.com/java/technologies/javase/javase8u211-later-archive-downloads.html)
- [Java7下载](https://www.oracle.com/java/technologies/javase/javase7-archive-downloads.html)
- [Deepin安装Java17示例](https://bbs.deepin.org/post/236160)
- [命令行安装deb包教程](https://blog.csdn.net/oMcLin/article/details/108725325)

#### Arch特编

希望不要滚挂:
``pacman -Syyu``

##### OpenJDK安装

- JDK18(jdk18-openjdk)`<sup>`[AUR](https://aur.archlinux.org/packages/jdk18-openjdk) `</sup>`
- JDK17(jdk-temurin)`<sup>`[AUR](https://aur.archlinux.org/packages/jdk17-temurin) `</sup>`
- JDK16(jdk16-openjdk)`<sup>`[AUR](https://aur.archlinux.org/packages/jdk16-openjdk) `</sup>`
- JDK8(jdk8-openjdk-shenandoah)`<sup>`[AUR](https://aur.archlinux.org/packages/jdk8-openjdk-shenandoah) `</sup>`
- 可使用 ``yay -s (JDK名字后面的括号里的内容，不要带上括号)``来安装对应版本

环境配置至此完成

# 基本使用方法

- 开启服务器
  - 在主界面点击“开启服务器”即可
  - 注意事项
    - 必须事先选择服务端路径和服务端（服务端没有可以点击服务端路径和“...”选择路径中间的下载摁钮下载）
    - 必须配置好对应版本的Java,不知道如何配置可以点击主页下方的“如何选择”查看帮助
- 配置服务器
  - 主页提供了常用的服务器设置，如是否开启PVP，最大在线人数等
  - 进阶设置可以在服务端路径下的server.properties修改，每个选项的释义可以在[这里](#server.properties中部分常用配置翻译)查看
  - 服务端目录结构，开服前准备都可以在主界面-帮助查看

# 进阶设置和疑难解答

## 软件相关

- 服务器相关问题请自行Bing，不是软件的问题不要在仓库提交issues（除非你有好的建议）
- 参与讨论可以提交issues
- 改好了请直接提交PR，详细描述解决的是什么问题，咋解决的

### 使用自定义域名

您得先有一个域名，然后参照以下教程：

- [阿里云](https://doc.natfrp.com/#/app/mc?id=srv-aliyun)
- [腾讯云](https://doc.natfrp.com/#/app/mc?id=srv-tencent)
- [CloudFlare](https://doc.natfrp.com/#/app/mc?id=srv-cloudflare)

### 常用指令

- ``/ban <玩家名/玩家IP地址>  封禁玩家名/玩家IP地址``
- ``/kick <玩家名/玩家IP地址>  临时踢出玩家名/玩家IP地址``

### server.properties中部分常用配置翻译

``int``代表一个整数

``str``代表一串字符

`bool`代表您只能选择True(是)或者Flase(否)作为值

| 类型     | 名称                                  | 释义                                                                                     |
| -------- | ------------------------------------- | --------------------------------------------------------------------------------------- |
| `bool`   | `sync-chunk-writes`                 | 为true时区块文件以同步模式写入(跟本地一样加载)                                               |
| `bool`   | `force-gamemode`                    | 强制玩家加入时为默认游戏模式                                                                |
| `bool`   | `allow-nether`                      | 是否允许下界                                                                               |
| `bool`   | `enforce-whitelist`                 | 在服务器上强制使用白名单                                                                    |
| `bool`   | `spawn-monsters`                    | 生成攻击型生物（怪物）                                                                      |
| `bool`   | `pvp`                               | 是否允许玩家互相攻击                                                                        |
| `bool`   | `hardcore`                          | 极限模式（死后自动封禁）                                                                    |
| `bool`   | `enable-command-block`              | 启用命令方块                                                                               |
| `bool`   | `spawn-npcs`                        | 是否生成村民和其他NPC                                                                       |
| `bool`   | `allow-flight`                      | 是否允许玩家飞行                                                                            |
| `bool`   | `generate-structures`               | 生成世界时生成结构（如村庄）禁止后地牢和地下要塞仍然生成                                       |
| `bool`   | `online-mode`                       | Minecraft正版验证                                                                          |
| `bool`   | `white-list`                        | 是否开启白名单                                                                             |
| `bool`   | `prevent-proxy-connections`         | 是否允许玩家使用网络代理进入服务器                                                           |
| `bool`   | `use-native-transport`              | 是否使用针对Linux平台的数据包收发优化 (仅Linux)                                              |
| `int`    | `spawn-protection`                  | 通过将该值进行 2x+1 的运算来决定出生点的保护半径，设置为0将只保护出生点下方那一个方块。          |
| `int`    | `max-tick-time`                     | 设置每个tick花费的最大毫秒数，超时会报错”Can't keep up!“                                     |
| `int`    | `query.port`                        | 服务器的端口号                                                                             |
| `int`    | `gamemode`                          | 默认游戏模式 [0生存 1创造 2冒险 3旁观]                                                      |
| `int`    | `player-idle-timeout`               | 允许的挂机时间，单位为分钟，超过后自动踢出                                                    |
| `int`    | `difficulty`                        | 世界难度 [0和平 1简单 2普通 3困难]                                                          |
| `int`    | `op-permission-level`               | OP权限等级                                                                                 |
| `int`    | `entity-broadcast-range-percentage` | 实体渲染范围百分比                                                                          |
| `int`    | `max-players`                       | 服务器最大玩家数限制                                                                        |
| `int`    | `network-compression-threshold`     | 网络压缩阈值                                                                               |
|          |                                     | -1 代表禁用压缩                                                                            |
|          |                                     | 0 代表全部压缩                                                                             |
|          |                                     | 数字越大越节省带宽，但同时也会加重CPU负担                                                    |
| `int`    | `max-world-size`                    | 最大世界大小                                                                               |
| `int`    | `function-permission-level`         | 设定函数的默认权限等级                                                                      |
| `int`    | `server-port`                       | 服务器端口                                                                                 |
| `int`    | `server-ip`                         | 服务器ip，若不绑定请留空                                                                    |
| `int`    | `view-distance`                     | 服务器发送给客户端的数据量，决定玩家能设置的视野                                              |
| `int`    | `level-seed`                        | 地图种子                                                                                   |
| `str`    | `generator-settings`                | 用于自定义超平坦世界的生成                                                                  |
| `str`    | `level-type`                        | 地图的生成类型                                                                             |
| `str`    | `level-name`                        | 地图名称，不要使用中文                                                                      |
| `str`    | `resource-pack`                     | 统一资源标识符 (URI) 指向一个资源包。玩家可选择是否使用                                        |
| `str`    | `motd`                              | 服务器信息展示 （MOTD）                                                                     |

- 更多详见[Minecraft Wiki](https://minecraft.fandom.com/zh/wiki/Server.properties?variant=zh)

### 使用Nginx进行反向代理

#### 什么是Nginx

Nginx (读作"engine X") 由Igor Sysoev(俄罗斯)于2005年编写，是一个免费、开源、高性能的HTTP服务器和反向代理，也可以作为一个IMAP/POP3代理服务器。Nginx因为稳定，丰富的功能集，配置简单，资源占用低而闻名世界。

#### 安装

##### 使用apt安装

```bash
sudo apt install nginx
sudo systemctl status nginx
```

> 在安装完成后，请确认防火墙已放通需要的端口。云服务器还需要配置安全组策略。具体方法请自行搜索，此处不再赘述。

##### 使用编译方式

###### 下载依赖

- ``sudo apt install build-essential libpcre3 libpcre3-dev zlib1g-dev unzip git openssl libssl-dev``
- 访问[Nginx官网下载地址](https://nginx.org/en/download.html)，下载最新Mainline版本的Nginx。截至这篇文章编写(2023/8/22)，最新Mainline版本为1.25.2，本篇将以这个版本作示例。
- ```bash
  curl -O https://nginx.org/download/nginx-1.25.2.tar.gz &&  tar -zxvf nginx-1.25.2.tar.gz
  ```

  > 可选组件
  >

  - OpenSSL

  ```bash
  curl -O https://www.openssl.org/source/openssl-3.1.2.tar.gz && tar -zxvf openssl-3.1.2.tar.gz
  ```

  - Brotli

  ```bash
  git clone https://github.com/google/ngx_brotli.git
  cd ngx_brotli
  git submodule update --init
  cd ..
  ```

###### 开始编译

> 切换到nginx源码目录

```bash
cd nginx-1.25.2
```

> 查看可用编译选项

```bash
./configure --help
```

> 编译

> user和group分别为用户和用户组，需要自己根据本机情况替换。如果需要指定安装目录和配置文件目录可以分别指定 ``--prefix``和 ``--conf-path``参数。
> Nginx默认的安装目录为/usr/local/nginx/，配置文件为/usr/local/nginx/conf/nginx.conf。

```bash
./configure --user=www-data --group=www-data --add-module=../ngx_brotli --with-openssl=../openssl-3.1.2  --with-openssl-opt='enable-tls1_3' --with-http_v2_module --with-http_ssl_module --with-http_gzip_static_module --with-http_realip_module --with-http_stub_status_module --with-stream && sudo make && sudo make install
```

#### Arch特编

##### 使用Pacman

```bash
pacman -S nginx-mainline
systemctl status nginx
```

> 如果未启动请务必启动

```bash
sudo systemctl start nginx
```

> 设置开机自启

```bash
sudo systemctl enable nginx
```

> 检查nginx版本，没有报错即为成功

```bash
nginx -V
```

##### 编译安装

Archlinux下编译安装的方法基本和Ubuntu一致。
可以这么启动nginx：

```bash
cd /usr/local/nginx/sbin && ./nginx
```

# 关于

[![OSCS Status](https://www.oscs1024.com/platform/badge/MojaveHao/MSL-X.svg?size=large)](https://old.murphysec.com/dr/uKTcHf4KwdbSC0tFFC)

MSLX
Code by MojaveHao

Copyright MojaveHao

Open Source License:GNU Affero Genral Public License v3([View at there](https://www.gnu.org/licenses/agpl-3.0.en.html))

## More

__不鼓励且不支持所有商业用途__
未经许可，**任何人**不得将本文开头关于MSLX名称由来介绍的图片、图标或原文用于商业目的或项目首页，或其他未经授权的行为。

衍生软件**需要**声明引用
如果在**没有修改**的情况下引用了 MSL-X 分发包，则派生项目应在描述的任何位置**提及 MSLX 的使用**。
如果修改并重新发布 MSL-X 源代码，或发布其他项目参考 MSL-X 的内部实现，则**必须**在文章开头或MSLX相关内容**最先出现**（https://github.com/MojaveHao/MSL-X）。 __不得歪曲或隐藏它是免费和开源的事实__。

__Discourages__ and does __not support all commercial__ use
Without permission, __no one__ may use images and icons, or the original text of the introduction about the origin of the name MSLX at the beginning of this article, for commercial purposes or on the homepage of the project, or other unauthorized acts.

Derivative software __needs__ to declare reference
If the MSL-X distribution package is referenced __without modifying it__, the derived project should __mention the use of MSLX__ anywhere in the description.
If the MSL-X source code is modified and republished, or another project is published with reference to the internal implementation of MSL-X, the derivative project __must__ be clearly declared from this repository at the beginning of the article or where the 'MSL-X' related content first __appears__ (https: //github.com/MojaveHao/MSL-X). The fact that __it is free and open source must not be distorted or hidden__.

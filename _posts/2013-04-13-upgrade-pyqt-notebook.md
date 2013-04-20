---
layout: post
title: "PyQt 升级笔记"
description: "<p>昨天下午，Bingal 发给我一个小程序，PyQt 编写的网页测试工具，支持 Retina 显示，比我之前 Hello World 的那些小对话框，效果要好上不少。于是我问，他用的是什么版本，他告诉我是最新的 5.0.1，并发来了链接。</p><p>打开 Qt 官网，发现已经升级至 5.0.2 了，心中窃喜，难道是因为新的 Qt 版本，实现了对 Retina 的支持？虽然眼看将要下班，还是忍不住升级。</p>"
category: pyqt
tags: [python, pyqt]
---
{% include JB/setup %}

昨天下午，Bingal 发给我一个小程序，PyQt 编写的网页测试工具，支持 Retina 显示，比我之前 Hello World 的那些小对话框，效果要好上不少。于是我问，他用的是什么版本，他告诉我是最新的 5.0.1，并发来了链接。

打开 Qt 官网，发现已经升级至 5.0.2 了，心中窃喜，难道是因为新的 Qt 版本，实现了对 Retina 的支持？虽然眼看将要下班，还是忍不住升级。

之前尝试 PyQt 的时候，嫌源码安装麻烦，偷懒用了 [HomeBrew](http://mxcl.github.io/homebrew/):

`$ brew install pyqt`

通过日志可知，依次安装了以下程序：

* sip-4.13.3
* qt-4.8.4
* PyQt-mac-gpl-4.9.4

很方便，但因为环境变量的关系，我只能通过控制台启动 Qt 程序，PyCharm 找不到 PyQt4。加上不支持 Retina，我也就一直没再折腾。

现在，动力来了！

----

### 卸载 PyQt 4.9.4

`$ brew uninstall pyqt`

瞬间完成。

### 下载并安装 Qt 5.0.2

[下载地址](http://qt-project.org/downloads) Qt 5.0.2 for Mac (404 MB) 

已经编译好，通过图形界面安装，没有悬念。不过你要记住安装的路径。

### 下载并编译安装 PyQt 4.10	

[下载地址](http://www.riverbankcomputing.co.uk/software/pyqt/download)

注意官网新闻：

PyQt v4.10 1 March 2013

>PyQt v4.10 has been released. This is the first release that supports Qt v5.0.

相对大个头的 Qt，PyQt 的下载要快多了。但是解压编译出错，报 SIP 的版本过低。

于是下载最新的 4.14.5，安装之后，故障依旧，心知这是 brew 的原因，但不敢用 brew 来卸载，这似乎是很多程序都依赖的公共包？

想了各种办法，将系统环境变量里的 SIP 更新为 4.14.5，以至于控制台 `SIP -V` 命令，能正确输出 4.14.5，configure 还是报错，卡在这里至少一个小时。

后来参考[这个文章](http://www.noktec.be/python/how-to-install-pyqt4-on-osx)

用下面的命令重新安装 SIP：

```
$ python configure.py -d /usr/local/lib/python2.7/site-packages
$ make
$ sudo make install
```

然后编译 PyQt

`$ python configure.py`

通过！

接下来 `make`，悲剧发生了，从控制台的输出看，make 的对象不是我新装的 Qt 5.0.2，还是旧版 4.8.4，而且编译的时间很长，我又不敢中断，只能等。错就错在我忘记卸载 Qt 4.8.4 了。

第二次 make 的时候，学乖了，也是受上面那篇文章的启发，指定了 Qt 路径：

`$ python configure.py -q /opt/Qt5.0.2/5.0.2/clang_64/bin/qmake`

但在安装的最后一步，还是出错：

`$ sudo make install`

这个错误，我到现在也没有搞明白，难道是权限的问题？一直提示找不到目标路径：

```
cp: /System/Library/Frameworks/Python.framework/Versions/2.7/share/sip/PyQt4/QtOpenGL/opengl_types.sip: No such file or directory
make[1]: *** [install] Error 1
make: *** [install] Error 2
```

没有办法，我只能手工建这些目录，算是复习 PyQt 的模块名称吧：

`$ sudo mkdir -p /System/Library/Frameworks/Python.framework/Versions/2.7/share/sip/PyQt4/QtOpenGL`

如此往复十几次，总算安装成功。

启动 PyCharm，发现已经自动找到了 PyQt4，程序正常运行。

但是，但是，字体还是虚的！

检查各组件版本，没有问题：

```python
# Getting the version numbers of Qt, SIP and PyQt

# When you report a bug in PyQt you need to supply information about the configuration you are using,
# including the versions of the Qt library, SIP and PyQt modules.
# The following code should help.


from PyQt4.QtCore import QT_VERSION_STR
from PyQt4.pyqtconfig import Configuration

print("Qt version:", QT_VERSION_STR)

cfg = Configuration()
print("SIP version:", cfg.sip_version_str)
print("PyQt version:", cfg.pyqt_version_str)
```

输出结果：

```
('Qt version:', '5.0.2')
('SIP version:', '4.14.5')
('PyQt version:', '4.10')
```

痛苦还没有结束！

### 让 Qt 支持 Retina

网上搜索 Qt Retina，有不少结果，诸如：

[Qt Creator on MacBook Pro Retina](http://www.qtcentre.org/threads/50130-Qt-Creator-on-MacBook-Pro-Retina)

昨天看的那篇，印象比较深刻，是一个邮件列表，似乎是说在他妻子的 Mac 上测试成功了，方法是修改 info.plists。

```xml
<key>NSPrincipalClass</key>
    <string>NSApplication</string>
<key>NSHighResolutionCapable</key>
    <true/>
```

修改这个文件以支持 Retina 屏，这个我并不陌生，Eclipse 也需要这么整才不模糊。

但是当时我不得要领，心想，我就是一个简单的 hello.py 哪里有 info.plists 可修改？

直到我找这个文章：

[Qt applications are blurry on MBP Retina](https://trac.macports.org/ticket/36410)

ticket 中提到了这个路径：

`/opt/local/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/Info.plist`

我才开窍，找到自己对应的地址，修改之，也倒腾了很久，原因是有个技巧：

>making a copy (in the finder by dragging, don't know if cp -r will work) and then renaming the original to python.app to python.app.old in the finder and renaming the copy to python.app . Starting spyder (a pyqt application) from the terminal now launches it in high-res.

大多数网友反馈，修改之后，文字支持高清了，但是图片还要另行处理，比如：

>Text render ok. Image need render 2x image to 1x QRect() (ex QPainter.drawImage(QRect(1x), QImage(2x)))

详情见[这里](https://bugreports.qt-project.org/browse/QTBUG-23870)。

以后要处理图片/图标的时候，再详细研究。

----

现在读这些文字，感觉也不怎么复杂，但当时身在其中，非常痛苦，每一步挫折，都让我产生了中途放弃的冲动，幸运的是最终我坚持下来了。

成功解决以下问题：

1. 编译安装 Qt，学会了不少命令，各个组件，都升级到了最新版本；

2. 环境变量可控，PyCharm 可直接运行 PyQt 程序。正直要写浏览器，还是少不了 IDE 支持； 

3. 文本不再模糊了； 

4. 直接推动我升级 PyCharm，PhpStorm，RubyMine 和 AppCode 至最新版本，Bug 修复、新功能增强等不再话下，还有了漂亮的 Durcula 主题；

5. 发现了 PyCharm 对 Emmet 的完美支持，运行、调试 HTML 文件，也非常方便； 

6. 下定决心，以后多看 Intellij Idea 的[官方文档](http://www.jetbrains.com/idea/webhelp/getting-help.html)；

7. 支持 Retina，不是因为我升级了 PyQt，而是 info.plists 的功劳。




















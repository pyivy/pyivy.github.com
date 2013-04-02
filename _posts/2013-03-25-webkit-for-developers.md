---
layout: post
title: "开发者需要了解的 WebKit"
description: "<p>对许多开发者来说，WebKit 就像一个黑盒。我们把 HTML、CSS、JS 和其他一大堆东西丢进去，然后 WebKit 魔法般的以某种方式把一个看起来不错的网页展现给我们。但事实上，Paul 的同事 Ilya Grigorik 说：</p><p>WebKit 才不是个黑盒。它是个白盒。并且，它是个打开的白盒。</p>"
category: python
tags: [webkit]
---
{% include JB/setup %}


[作者](http://paulirish.com/about/) | [Resume](http://paulirish.com/resume.html)

[中译](http://www.infoq.com/cn/articles/webkit-for-developers) | [Original](http://paulirish.com/2013/webkit-for-developers/)

Paul Irish 是著名的前端开发工程师，同时他也是 Chrome 开发者关系团队成员，jQuery 团队成员，Modernizr、 Yeoman、CSS3 Please 和 HTML5 Boilerplate 的 lead developer。针对大家对 WebKit 的种种误解，他在自己的博客发表了《WebKit for Developers》一文，试图为大家解惑。

 
对许多开发者来说，WebKit 就像一个黑盒。我们把 HTML、CSS、JS 和其他一大堆东西丢进去，然后 WebKit 魔法般的以某种方式把一个看起来不错的网页展现给我们。但事实上，Paul 的同事 Ilya Grigorik 说：

>WebKit 才不是个黑盒。它是个白盒。并且，它是个打开的白盒。

[Webkit in Google docs](https://docs.google.com/presentation/d/1ZRIQbUKw9Tf077odCh66OrrwRIVNLvI_nhLm2Gi__F0/edit#slide=id.p)

所以让我们来花些时间了解这些事儿：

* 什么是 WebKit？
* 什么不是 WebKit？
* 基于 WebKit 的浏览器是如何使用 WebKit 的？
* 为什么又有不同的 WebKit？

现在，特别是 Opera 宣布将浏览器引擎转换为 WebKit 之后，我们有很多使用 WebKit 的浏览器，但是我们很难去界定它们有哪些相同与不同。下面我争取为这个谜团做些解读。而你也将会更懂得判断浏览器的不同，了解如何在正确的地方报告 Bug，还会了解如何在特定浏览器下高效开发。


## 标准 Web 浏览器组件

让我们列举一些现代浏览器的组件：

* HTML、XML、CSS、JavsScript解析器
* Layout
* 文字和图形渲染
* 图像解码
* GPU交互
* 网络访问
* 硬件加速

这里面哪些是 WebKit 浏览器共享的？差不多只有前两个。其他部分每个 WebKit 都有各自的实现，所谓的 `port`。现在让我们了解一下这是什么意思……

## WebKit Ports 是什么

在 WebKit 中有不同的`port`，但是这里允许我来让 WebKit hacker，Sencha 的工程主管 Ariya Hidayat 来解释：

>WebKit 最常见的参考实现是 Apple 在 Mac OS X 上的实现（这也是最早和最原始的 WebKit 库）。但是你也能猜到，在 Mac OS X 下，许多不同的接口在很多不同的原生库下被实现，大部分集中在 CoreFoundation。举例来说，如果你定义了一个纯色圆角的按钮，WebKit 知道要去哪里，也知道要如何去绘制这个按钮。但是，绘制按钮的工作最终还是会落到 CoreGraphics 去。

上面已经提到，CoreGraphics 只是 Mac port 的实现。不过 Mac Chrome 用的是 Skia。

>随时间推移，WebKit 被`port`（移植）到了各个不同的平台，包括桌面端和移动端。这种做法被称作`WebKit port`。对 Windows 版 Safari 来说，Apple 通过（有限实现的）Windows 版本 CoreFoundation 来 port WebKit。

……不过 Windows 版本的 Safari 现在[已经死掉了](http://www.macworld.com/article/1167904/safari_6_available_for_mountain_lion_and_lion_but_not_windows.html)。

>除此之外，还有很多很多其它的`port`（[参见列表](http://trac.webkit.org/wiki#WebKitPorts)）。Google 创建并维护着它的 Chromium port。这其实也是一个基于 Gtk+ 的 WebKitGtk。诺基亚通过收购 Trolltech，维护着以 QtWebKit module 而闻名的 WebKit Qt port。

让我们看看其中一些WebKit ports：

1、Safari

* OS X Safari 和 Windows Safari 使用的是不同的 port
* 用于 OS X Safari 的 WebKit Nightly 以后会渐渐成为一个边缘版本

2、Mobile Safari

* 在一个私有代码分支上维护，不过代码现在正在合并到主干
* iOS Chrome（使用了 Apple 的 WebView，不过后面的部分有很多不同）

3、Chrome（Chromium）

* 安卓 Chrome（直接使用 Chromium port）
* Chromium 也驱动了 Yandex Browser、 360 Browser、Sogou Browser，很快，还会有 Opera。

4、还有很多： Amazon Silk、Dolphin、Blackberry、QtWebKit、WebKitGTK+、The EFL port (Tizen)、wxWebKit、WebKitWinCE……


不同的 port 专注于不同的领域。Mac 的 port 注意力集中在浏览器和操作系统的分割上，允许把 ObjectiveC 和 C++ 绑定并嵌入原生应用的渲染。Chromium 专注在浏览器上。QtWebKit 的 port 在他的跨平台 GUI 应用架构上给 apps 提供运行时环境或者渲染引擎。

## WebKit 浏览器共享了那些东西

首先，让我们来看看这些 WebKit ports 的共同之处：

作者注：很有意思，这些内容我写了很多次，每次 Chrome 团队成员都给我纠正错误，正如你看到的……

1. WebKit 在使用相同的方式解析 WebKit。—— 实际上，Chrome 是唯一支持多线程 HTML 解析的 port。

2. 一旦解析完成，DOM 树也会构建成相同的样子。—— 实际上 Shadow DOM 只有在 Chromium 才被开启。所以 DOM 的构造也是不同的。自定义元素也是如此。

3. WebKit 为每个人创建了`window`对象和`document`对象。—— 是的，尽管它暴露出的属性和构造函数可以通过 feature flags 来控制。

4. CSS 解析都是相同的。将 CSS 解析为对象模型是个相当标准的过程。——不过，Chrome 只支持`-webkit-`前缀，而 Apple 和其他的 ports 支持遗留的`-khtml-`和`-apple-`前缀。

5. 布局定位？这些是基本生计问题啊！—— 尽管 Sub-pixel layout 和 saturated layout 算法是 WebKit 的一部分，不过各个 port 的实现效果还是有很多不同。

所以，情况很复杂。

就像 Flickr 和 GitHub 通过 flag 标识来实现自己的功能一样，WebKit 也有相同处理。这允许各个 port 自行决定是否启用 WebKit 编译特性标签的各种功能。通过命令行开关，或者通过`about:flags`还可以控制是否通过运行时标识来展示功能特性。

好，现在让我们再尝试一次搞清楚WebKit究竟有哪些相同。

## 每个 WebKit port 有哪些共同之处

* DOM、winow、document
* CSS 对象模型
* CSS 解析，键盘事件处理
* HTML 解析和 DOM 构建
* 所有的布局和定位
* Chrome 开发工具和 WebKit 检查器的 UI 与检查器
* contenteditable、pushState、文件 API、大多数 SVG、CSS Transform math、Web Audio API、localStorage 等功能
* [很多其他功能与特性](http://trac.webkit.org/browser/trunk/Source/WebCore)

这些领域现在有点儿模糊，让我们尝试把事情弄得更清楚一点。

## 什么是 WebKit port 们并没有共享的

* GPU 相关技术

  3D 转换

  WebGL

  视频解码

* 将 2D 图像绘制到屏幕

  解析方式

  SVG 和 CSS 渐变绘制

* 文字绘制和断字

* 网络层（SPDY、预渲染、WebSocket 传输）

* JavaScript 引擎

  JavaScriptCore 在 WebKit repo 中

  V8 和 JavaScriptCore 被绑定在 WebKit 中

* 表单控制器的渲染

* `<video>`和`<audio>`的元素表现和解码实现

* 图像解码

* 页面导航 前进/后退

  pushState() 的导航部分

* SSL功能，比如 Strict Transport Security 和 Public Key Pins

让我们谈谈其中的2D图像部分： 根据port的不同，我们使用完全不同的库来处理图像到屏幕的绘制过程：


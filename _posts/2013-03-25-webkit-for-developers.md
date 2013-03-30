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

Paul Irish是著名的前端开发工程师，同时他也是Chrome开发者关系团队成员，jQuery团队成员，Modernizr、 Yeoman、CSS3 Please和HTML5 Boilerplate的lead developer。针对大家对WebKit的种种误解，他在自己的博客发表了《WebKit for Developers》一文，试图为大家解惑。

 
对许多开发者来说，WebKit就像一个黑盒。我们把HTML、CSS、JS和其他一大堆东西丢进去，然后WebKit魔法般的以某种方式把一个看起来不错的网页展现给我们。但事实上，Paul的同事Ilya Grigorik说：

>WebKit才不是个黑盒。它是个白盒。并且，它是个打开的白盒。

[Webkit in Google docs](https://docs.google.com/presentation/d/1ZRIQbUKw9Tf077odCh66OrrwRIVNLvI_nhLm2Gi__F0/edit#slide=id.p)

所以让我们来花些时间了解这些事儿：

* 什么是WebKit？
* 什么不是WebKit？
* 基于WebKit的浏览器是如何使用WebKit的？
* 为什么又有不同的WebKit？

现在，特别是Opera宣布将浏览器引擎转换为WebKit之后，我们有很多使用WebKit的浏览器，但是我们很难去界定它们有哪些相同与不同。下面我争取为这个谜团做些解读。而你也将会更懂得判断浏览器的不同，了解如何在正确的地方报告bug，还会了解如何在特定浏览器下高效开发。


## 标准Web浏览器组件

让我们列举一些现代浏览器的组件：

* HTML、XML、CSS、JavsScript解析器
* Layout
* 文字和图形渲染
* 图像解码
* GPU交互
* 网络访问
* 硬件加速

这里面哪些是WebKit浏览器共享的？差不多只有前两个。其他部分每个WebKit都有各自的实现，所谓的“port”。现在让我们了解一下这是什么意思……

## WebKit Ports是什么？

在WebKit中有不同的“port”，但是这里允许我来让WebKit hacker，Sencha的工程主管Ariya Hidayat来解释：

>WebKit最常见的参考实现是Apple在Mac OS X上的实现（这也是最早和最原始的WebKit库）。但是你也能猜到，在Mac OS X下，许多不同的接口在很多不同的原生库下被实现，大部分集中在CoreFoundation。举例来说，如果你定义了一个纯色圆角的按钮，WebKit知道要去哪里，也知道要如何去绘制这个按钮。但是，绘制按钮的工作最终还是会落到CoreGraphics去。

上面已经提到，CoreGraphics只是Mac port的实现。不过Mac Chrome用的是Skia。

>随时间推移，WebKit被“port”（移植）到了各个不同的平台，包括桌面端和移动端。这种做法被称作“WebKit port”。对Windows版Safari来说，Apple通过（有限实现的）Windows版本CoreFoundation 来port WebKit。

……不过Windows版本的Safari现在[已经死掉了](http://www.macworld.com/article/1167904/safari_6_available_for_mountain_lion_and_lion_but_not_windows.html)。

>除此之外，还有很多很多其它的“port”（参见列表）。Google创建并维护着它的Chromium port。这其实也是一个基于Gtk+的WebKitGtk。诺基亚通过收购Trolltech，维护着以QtWebKit module而闻名的WebKit Qt port。

让我们看看其中一些WebKit ports：

1、Safari

* OS X Safari和Windows Safari使用的是不同的port
* 用于OS X Safari的WebKit Nightly以后会渐渐成为一个边缘版本

2、Mobile Safari

* 在一个私有代码分支上维护，不过代码现在正在合并到主干
* iOS Chrome（使用了Apple的WebView，不过后面的部分有很多不同）

3、Chrome（Chromium）

* 安卓Chrome（直接使用Chromium port）
* Chromium也驱动了Yandex Browser、 360 Browser、Sogou Browser，很快，还会有Opera。

4、还有很多： Amazon Silk、Dolphin、Blackberry、QtWebKit、WebKitGTK+、The EFL port (Tizen)、wxWebKit、WebKitWinCE……


不同的port专注于不同的领域。Mac的port注意力集中在浏览器和操作系统的分割上，允许把ObjectC和C++绑定并嵌入原生应用的渲染。Chromium专注在浏览器上。QtWebKit的port在他的跨平台GUI应用架构上给apps提供运行时环境或者渲染引擎。

待续...





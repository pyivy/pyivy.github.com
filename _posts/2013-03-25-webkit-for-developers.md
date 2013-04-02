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

让我们谈谈其中的 2D 图像部分： 根据 port 的不同，我们使用完全不同的库来处理图像到屏幕的绘制过程：

![graphics context](/assets/images/2013/02/graphicscontext.png)

更宏观一点来看，一个最近刚添加的功能：CSS.supports()在除了没有 css3 特性检测功能的 win 和 wincairo 这两个 port 之外，在其它所有 port 中都[可用](http://trac.webkit.org/changeset/142739)。

现在到了卖弄学问的技术时间。上面讲的内容其实并不正确。事实上那是 WebCore 被共享的东西。而 WebCore 其实是当大家讨论 HTML 和 SVG 的布局、渲染和 DOM 处理时提到的 WebKit。技术上讲，WebKit 是 WebCore 和各种 ports 之间的绑定层，尽管通常来说这个差别并不那么重要。

一个图表应该可以帮助大家理解：

![webkit diagram](/assets/images/2013/02/webkit-diagram.png)

WebKit 中的许多组件都是可以更换的（图中标灰色的部分）。

举个例子来说，Webkit 的 JavaScript 引擎，JavaScriptCore，是 WebKit 的默认组件。（它最初是当 WebKit 从 KHTML 分支时从 KJS 演变来的）。同时，Chromium port 用 V8 引擎做了替换，还使用了独特的 DOM 绑定来映射上面的组件。

字体和文字渲染是平台上的重要部分。在 WebKit 中有两个独立的文字路径：Fast 和 Complex。这两者都需要平台特性的支持，但是 Fast 只需要知道如何传输字型，而 Complex 实际上需要掌握平台上所有的字符串，并说“请绘制这个吧”。

>"WebKit 就像一个三明治。尽 Chromium 的包装更像是一个墨西哥卷。一个美味的 Web 平台墨西哥卷。"
—— Dimitri Glazkov, Chrome WebKit hacker，Web Components和 Shadow DOM 拥护者。

现在，让我们放宽镜头看看一些 port 和一些子系统。下面是 WebKit 的 5 个 port；尽管它们共享了 WebCore 的大部分，但考虑一下它们的 stack 有哪些不同。

<table class="table table-bordered table-hover table-striped">
    <tbody>
        <tr>
            <td>&nbsp;</td>
            <th>Chrome (OS X)</th>
            <th>Safari (OS X)</th>
            <th>QtWebKit</th>
            <th>Android Browser</th>
            <th>Chrome for iOS</th>
        </tr>
        <tr>
            <th>Rendering</th>
            <td>Skia</td>
            <td>CoreGraphics</td>
            <td>QtGui</td>
            <td>Android stack/Skia</td>
            <td>CoreGraphics</td>
        </tr>
        <tr>
            <th>Networking</th>
            <td>Chromium network stack</td>
            <td>CFNetwork</td>
            <td>QtNetwork</td>
            <td>Fork of Chromium’s network stack</td>
            <td>Chromium stack</td>
        </tr>
        <tr>
            <th>Fonts</th>
            <td>CoreText via Skia</td>
            <td>CoreText</td>
            <td>Qt internals</td>
            <td>Android stack</td>
            <td>CoreText</td>
        </tr>
        <tr>
            <th>JavaScript</th>
            <td>V8</td>
            <td>JavaScriptCore</td>
            <td>JSC (V8 is used elsewhere in Qt)</td>
            <td>V8</td>
            <td>JavaScriptCore (without JITting) *</td>
        </tr>
    </tbody>
</table>

*iOS Chrome 注：你可能知道它使用 UIWebView。由于 UIWebView 的能力限制。它只能使用移动版 Safari 的渲染层，JavaScriptCore（而不是 V8）和单进程模式。然而，大量的 Chromium 代码还是起到了调节作用 ，比如网络层、同步、书签架构、地址栏、度量工具和崩溃报告。（同时，由于 JavaScript 很少成为移动端的瓶颈，缺少 JIT 编译器只有很小的影响。）

## 好吧，那么我们该怎么办

现在所有 WebKit 完全不同了，我好怕。

别这样！WebKit 的 layoutTests 覆盖面非常广（据最新统计，有 28,000 个 layoutTests），这些 test 不仅针对已存在的特性，而且针对任何发现的回归。实际上，每当你探索一些新的或难懂的 DOM/CSS/HTML5 特性时，在整个 web 平台上，layoutTests 经常已经有了一些奇妙的小 demo。

另外，W3C 正在努力研究一致性测试套件。这意味着我们可以期待使用同一个测试套件来测试不同的 WebKit port 和浏览器，以此来获得更少的怪异模式，和一个带来更少的怪癖模式和更具互操作性的 web。对所有参加过 Test The Web Forward 活动的人们……致谢！

## Opera 刚刚迁移到了 WebKit 了

Robert Nyman 和 Rob Hawkes也谈到了这个 ，但是我会再补充一些：Opera 在公告中明显指出 Opera 将采用 Chromium。这意味着 WebGL，Canvas，HTML5 表单，2D 图像实现—— Chrome 和 Opera 将在所有这些功能上保持一致。API 和后端实现也会完全相同。由于 Opera 是基于 Chromium，你可以有足够的信心去相信你的尖端工作将会在 Chrome 和 Opera 上获得兼容。

我还应该指出，所有的 Opera 浏览器都将采用 Chromium：包括他的 Windows，Mac、Linux 版本，和 Opera Mobile（完全成熟的移动浏览器）。甚至 Opera Mini 都将使用基于 Chromium 的服务器渲染集群来替换当前的基于 Presto 的服务器端渲染。

## 那 WebKit Nightly 是什么 

它是 WebKit 的 mac port ，和 Safari 运行的二进制文件一样（尽管会替换一些底层库）。因为苹果在项目中起主导地位，所以它的表现和功能与 Safari 的总是那么一致。在很多情况下，当其它 port 可能会试验新功能的时候，Apple 却显得相对保守。不管怎样，如果你想我用中学一样的类比，想想这个好了：WebKit Nightly 对于 Safari 就像 Chromium 对于 Chrome。

同样的，Chrome Canary 有着最新的 WebKit 资源。

告诉我更多的 WebKit 内幕吧。

就在这儿了，小伙子：

<a href="https://docs.google.com/presentation/d/1ZRIQbUKw9Tf077odCh66OrrwRIVNLvI_nhLm2Gi__F0/embed?start=false&amp;loop=false&amp;delayms=3000"> <img src="http://paulirish.com/i/x3fb890.png.pagespeed.ic.6nLbkKT48f.png" alt="" _href="http://paulirish.com/i/x3fb890.png.pagespeed.ic.6nLbkKT48f.png" _p="true"> </a>

## 扩展阅读

* [WebKit internals technical articles | webkit.org](http://www.webkit.org/coding/technical-articles.html)

* [WebKit: An Objective View | Robert Nyman & Rob Hawkes](http://robertnyman.com/2013/02/14/webkit-an-objective-view/) 译者注：InfoQ 发布的[中文译文](http://www.infoq.com/cn/news/2013/02/webkit-history-and-now)

* [your webkit port is special (just like every other port) | Ariya Hidayat](http://ariya.ofilabs.com/2011/06/your-webkit-port-is-special-just-like-every-other-port.html)

* [Getting Started With the WebKit Layout Code | Adobe Web Platform Blog](http://blogs.adobe.com/webplatform/2013/01/21/getting-started-with-the-webkit-layout-code/)

* [WebKit Documentation Overview | Arun Patole](http://arunpatole.com/blog/2011/webkit-documentation/)

* [Rendering in WebKit, by Eric Seidel | YouTube](http://www.youtube.com/watch?v=RVnARGhhs9w)

* [web performance for the curious | Ilya Grigorik](http://www.igvita.com/slides/2012/web-performance-for-the-curious/)

* [WebKit is the jQuery of Browser Engines | John Resig](http://ejohn.org/blog/webkit-is-the-jquery-of-browser-engines/)

* [The Great WebKit Comparison Table | PPK](http://www.quirksmode.org/webkit.html)

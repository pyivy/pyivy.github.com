---
layout: post
title: "如何只用一个加号计算三个数之和"
description: "<p>这是在 <a href='http://segmentfault.com/q/1010000000186540'>SegmentFault</a> 上看到的一个问题，小时也经常玩类似的游戏，比如，如何只移动一根火柴，使等式成立？</p><p>具体请 Google。</p><p><img src='/assets/images/2013/02/match.jpg' alt='火柴'></p><p>我学编程，是直接从 JSP 入手的，从未接受过位运算的训练，今天开眼界了。</p>"
category: program
tags: [plus, python, ipython]
---
{% include JB/setup %}

这是在 [SegmentFault](http://segmentfault.com/q/1010000000186540) 上看到的一个问题，小时也经常玩类似的游戏，比如，如何只移动一根火柴，使等式成立？

具体请 Google。

![火柴](/assets/images/2013/02/match.jpg)

我学编程，是直接从 JSP 入手的，从未接受过位运算的训练，今天开眼界了。

```
In [27]: a = 10

In [28]: b = 12

In [29]: c = 32

In [30]: ( a ^ b ^ c ) + ( ( ( a & b ) | ( b & c ) | ( a & c ) ) << 1 ) 

Out[30]: 54
```

6 的二进制是 110，11的二进制是 1011，那么 6 and 11 的结果就是 0010 --> 2。

```
In [6]: 6 & 11

Out[6]: 2
```

0 表示 False，1 表示 True，空位都当 0 处理。

Python 转换方法：

```
In [12]: bin(11)

Out[12]: '0b1011'


In [20]: int(0b110)

Out[20]: 6
```

学无止境。
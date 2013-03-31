---
layout: post
title: "在控制台打印各种三角形"
description: "<p>中午吃饭的时候，在 YouTube 上看了一个 15 分钟的 Python 视频，最基本的入门，变量，赋值，运算，函数，流程控制，基本是走马观花，不过毕竟只的 15 分钟，也是一个复习基础的机会。Python 真是一门易学的语言，但是，你只会这些，什么事情也做不了，所以，定一个项目做吧，哪怕是极其无聊的，比如我，突然想在控制台打印三角形。</p><p>知识点：function, string, if, while, for, range ...</p><p>起源呢，是视频作者演示 for + while 循环的时候，写的一个代码片断，打印一个直角三角形，由于精力不够集中，我自己写的，竟然打印出一个反方向的三角形，囧。受到刺激了，于是决定进一步学习，打印各种三角形。</p><p>先帖上原始代码，别笑话，我现在的 Python 水平就是这个样子，打酱油都不够格。</p>"
category: python
tags: [python]
---
{% include JB/setup %}

中午吃饭的时候，在 YouTube 上看了一个 15 分钟的 Python 视频，最基本的入门，变量，赋值，运算，函数，流程控制，基本是走马观花，不过毕竟只的 15 分钟，也是一个复习基础的机会。Python 真是一门易学的语言，但是，你只会这些，什么事情也做不了，所以，定一个项目做吧，哪怕是极其无聊的，比如我，突然想在控制台打印三角形。

知识点：function, string, if, while, for, range ...

起源呢，是视频作者演示 for + while 循环的时候，写的一个代码片断，打印一个直角三角形，由于精力不够集中，我自己写的，竟然打印出一个反方向的三角形，囧。受到刺激了，于是决定进一步学习，打印各种三角形。

先帖上原始代码，别笑话，我现在的 Python 水平就是这个样子，打酱油都不够格。

```python
def astarts(num):
	for x in range(num):
		while x >= 0:
			print '*',
			x -= 1
		print
	return

def dstarts(num):
	tmp = num - 1
	for x in range(tmp):
		while x < tmp:
			print '*',
			x += 1
		print
	return

y = 10
astarts(y)
dstarts(y)

print

print '* ' * 26
print '*', 'This scripts if written for print stars.'
print '* ' * 26
```

运行的结果是这样的：

```
*
* *
* * *
* * * *
* * * * *
* * * * * *
* * * * * * *
* * * * * * * *
* * * * * * * * *
* * * * * * * * * *
* * * * * * * * *
* * * * * * * *
* * * * * * *
* * * * * *
* * * * *
* * * *
* * *
* *
*
```

太无聊了，像信封，待续...


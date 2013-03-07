---
layout: post
title: "Hide Window with NirCmd"
description: ""
category: python
tags: [nircmd, os, sys, format, string, input]
---
{% include JB/setup %}

有的时候，出于安全或者是其它方面的原因，我们需要隐藏某些窗口，这里贴出我写的一小段代码，借助了 [NirCmd](http://www.nirsoft.net/utils/nircmd.html)。

{% highlight python %}
import sys
import os

u_input =  raw_input("Please enter the act:\n[H]ide or [S]how\n")
p_title =  raw_input("Please enter the title:\n")
u_act   =  u_input.lower()

if u_act == "h" or u_act == "hide":
	act = "hide"
elif u_act == "s" or u_act == "show":
	act = "show"
else:
	act = "hide"

str_command = "nircmd win %s ititle %s" % (act, p_title)
print str_command

os.popen(str_command)
print "done"
{% endhighlight %}


### 知识点
----


#### 1. 执行命令行

借助 [os](http://docs.python.org/2.7/library/os.html) 模块的 [popen()](http://docs.python.org/2.7/library/os.html#os.popen)方法

`os.popen(command[, mode[, bufsize]])`

注：官方文档提示，从Python 2.6 开始，该方法被标记为 *Deprecated* 。

推荐使用 [subprocess](http://docs.python.org/2.7/library/subprocess.html#module-subprocess)。

####  2. 与用户交互

借助 [sys](http://docs.python.org/2.7/library/sys.html) 模块

raw_input() & input()

这两个均是 Python 的内建函数，通过读取控制台的输入与用户实现交互。但他们的功能不尽相同。

示例代码：

{% highlight python %}
>>> raw_input_A = raw_input("raw_input: ")
 raw_input: abc
 >>> input_A = input("Input: ")
Input: abc
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1, in <module>
NameError: name 'abc' is not defined
{% endhighlight %}

{% highlight python %}
>>> raw_input_B = raw_input("raw_input: ")
 raw_input: 123
  >>> type(raw_input_B)
  <type 'str'>
 >>> input_B = input("input: ")
 input: 123
 >>> type(input_B)
 <type 'int'>
 >>>
{% endhighlight %}

*例子 1* 可以看到：这两个函数均能接收**字符串**，但 raw_input() 直接读取控制台的输入（任何类型的输入它都可以接收）。而对于 input() ，它希望能够读取一个合法的 Python 表达式，即你输入字符串的时候必须使用引号将它括起来，否则它会引发一个 SyntaxError 。

*例子 2* 可以看到：raw_input() 将所有输入作为字符串看待，返回字符串类型。而 input() 在对待纯数字输入时具有自己的特性，它返回所输入的数字的类型（ int, float ）；同时在 *例子 1* 知道，input() 可接受合法的 Python 表达式，举例：input( 1 + 3 ) 会返回 int 型的 4 。

查看 [Built-in Functions](http://docs.python.org/2/library/functions.html?highlight=input#built-in-functions) ，得知：


>input(\[prompt])
>>Equivalent to eval(raw_input(prompt))

input() 本质上还是使用 raw_input() 来实现的，只是调用完 raw_input() 之后再调用 eval() 函数，所以，你甚至可以将表达式作为 input() 的参数，并且它会计算表达式的值并返回它。

不过在 Built-in Functions 里有一句话是这样写的：Consider using the raw_input() function for general input from users.

除非对 input() 有特别需要，否则一般情况下我们都是推荐使用 raw_input() 来与用户交互。

#### 3. 字符串格式化

这里我用最传统的 “%” 运算符，与 C 中 sprintf 函数是一样的语法。

**通用的格式：**

>格式标记字符串 % 要输出的值组

转换类型表：

<table border="1" style="margin:0px;padding:0px;border:1px solid #C0C0C0;color:#333333;background-color:#FFFFFF;">
	<tbody>
		<tr>
			<th style="color:#000000;border:1px solid #C0C0C0;">
				格式
			</th>
			<th style="color:#000000;border:1px solid #C0C0C0;">
				描述
			</th>
		</tr>
	</tbody>
	<tbody>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%%
			</td>
			<td style="border:1px solid #C0C0C0;">
				百分号标记
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%c
			</td>
			<td style="border:1px solid #C0C0C0;">
				字符及其ASCII码
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%s
			</td>
			<td style="border:1px solid #C0C0C0;">
				字符串
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%d
			</td>
			<td style="border:1px solid #C0C0C0;">
				有符号整数(十进制)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%u
			</td>
			<td style="border:1px solid #C0C0C0;">
				无符号整数(十进制)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%o
			</td>
			<td style="border:1px solid #C0C0C0;">
				无符号整数(八进制)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%x
			</td>
			<td style="border:1px solid #C0C0C0;">
				无符号整数(十六进制)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%X
			</td>
			<td style="border:1px solid #C0C0C0;">
				无符号整数(十六进制大写字符)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%e
			</td>
			<td style="border:1px solid #C0C0C0;">
				浮点数字(科学计数法)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%E
			</td>
			<td style="border:1px solid #C0C0C0;">
				浮点数字(科学计数法，用E代替e)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%f
			</td>
			<td style="border:1px solid #C0C0C0;">
				浮点数字(用小数点符号)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%g
			</td>
			<td style="border:1px solid #C0C0C0;">
				浮点数字(根据值的大小采用%e或%f)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%G
			</td>
			<td style="border:1px solid #C0C0C0;">
				浮点数字(类似于%g)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%p
			</td>
			<td style="border:1px solid #C0C0C0;">
				指针(用十六进制打印值的内存地址)
			</td>
		</tr>
		<tr>
			<td style="border:1px solid #C0C0C0;">
				%n
			</td>
			<td style="border:1px solid #C0C0C0;">
				存储输出字符的数量放进参数列表的下一个变量中
			</td>
		</tr>
	</tbody>
</table>  


**格式化浮点数：**

{% highlight python %}
>>> str = "Pi with three decimals: %.3f"
>>> from math import pi
>>> print str % pi
Pi with three decimals: 3.142
{% endhighlight %}

另外，[string](http://docs.python.org/2/library/string.html) 模块提供了更完整的[字符串格式化方案](http://docs.python.org/2/library/string.html#string-formatting)，可从这里的[例子](http://docs.python.org/2/library/string.html#format-examples)看起。

 












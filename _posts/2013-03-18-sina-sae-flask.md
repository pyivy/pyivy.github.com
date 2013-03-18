---
layout: post
title: "Sina SAE Flask 项目搭建笔记"
description: "Sina SAE Flask 项目搭建笔记"
category: flask
tags: [flask, sina, sae]
---
{% include JB/setup %}

认识 Flask 很久了，对它的 Logo 记忆很深刻，小时候太喜欢吃辣了。

曾记得某位牛人总结为什么创业失败，提到：

`我应该去学习 Flask`

Sina SAE 内置了 Flask 框架，下面是官方的示例代码，以后再更新为有实际意义的应用。

## MySQL

{% highlight sql %}
CREATE TABLE  `app_uuid`.`demo` (
`id` INT( 11 ) NOT NULL AUTO_INCREMENT ,
`text` TEXT NOT NULL ,
PRIMARY KEY (  `id` )
) ENGINE = MYISAM ;

{% endhighlight %}

## index.wsgi

{% highlight python %}
import sae
from chenzixin import app
application = sae.create_wsgi_app(app)
{% endhighlight %}

## chenzixin.py

{% highlight python %}
#coding:utf8
 
import MySQLdb
from flask import Flask, g, request
 
app = Flask(__name__)
app.debug = True
 
from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)
 
@app.before_request
def before_request():
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT))
 
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'): g.db.close()
 
@app.route('/')
def hello():
    return "Hello, world! - Flask"
 
@app.route('/demo', methods=['GET', 'POST'])
def greeting():
    html = ''
 
    if request.method == 'POST':
        c = g.db.cursor()
        c.execute("insert into demo(text) values(%s)", (request.form['text']))
 
    html += """
    <form action="" method="post">
        <div><textarea cols="40" name="text"></textarea></div>
        <div><input type="submit" /></div>
    </form>
    """
    c = g.db.cursor()
    c.execute('select * from demo')
    msgs = list(c.fetchall())
    msgs.reverse()
    for row in msgs:
        html +=  '<p>' + row[-1] + '</p>'
 
    return html
{% endhighlight %}

## Test

访问：http://\[your_app_name].sinaapp.com/demo

全文完。
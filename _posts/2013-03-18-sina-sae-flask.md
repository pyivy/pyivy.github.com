---
layout: post
title: "Sina SAE Flask 项目搭建笔记"
description: "<p>认识 Flask 很久了，对它的 Logo 记忆很深刻，小时候太喜欢吃辣了。</p><p>曾记得某位牛人总结为什么创业失败，提到：</p><p>Should have learnt Flask before.</p><p>Sina SAE 内置了 Flask 框架，下面是官方的示例代码，以后再更新为有实际意义的应用。</p>"
category: flask
tags: [flask, sina, sae]
---
{% include JB/setup %}

认识 Flask 很久了，对它的 Logo 记忆很深刻，小时候太喜欢吃辣了。

曾记得某位牛人总结为[什么创业失败](http://www.oschina.net/translate/failed-entrepreneur)，提到：

>Should have learnt Flask before

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

----

[**Why have I failed as an entrepreneur ?**](http://blog.bahadir.io/posts/failed-entrepreneur.html)

* I knew everything.

* made a good sprint, but couldn't finish the run. No more oxygen/energy.

###General

* did not take care myself; emotionally and physically

* did not listen people very well. I've heard them but did not actually listen. I kept on talking and talking.
* being an expat and entrepreneur is somewhat crazy when you know you're going to have visa problems. Too much instability in one man's life drains too much energy.
* did not use my time wisely
* tried to do too much
* should be less harsh on myself and others
* was(am) stubborn when I should not be
* was inconsistent ( ran ~90km in June '12 then in the last 6 months I only ran 30km )
* did not ask for help

###Business

* never did true problem description. Should have write it down

* should have connected with more people. Relationships matter a lot.
* did not plan ahead the business
* do not write a 100 page business plan does not mean don't write it at all
* started working on other ideas and lost focus when business needed the most
* should take the money when a beta user offered to pay
* should have postpone opening company till we have a paying customer base.
* should have asked money from people
* rather than having a $400 Amazon EC2 instance, €30 p/m server was enough.

###Programming

* scalability problems should be solved when there are scalability problems.

* have stuck in maker's obsession
* wrote too much code. 30% became immediately unnecessary
* did not prioritize what I should be working next
* should have learnt Celery before
* should have learnt Flask before
* more Backbone less spagetti JS.
* less code, less code, less code.
* my job is not programming. My job is delivering value using programming.


###The Product

* should release the app much more earlier

* should have fixed the showstopper bug and email users a.s.a.p. to say that we're sorry. ( Some users registered and tried the app when they shouldn't but since I left the Google login open, they've registered and saw a non-working app )
* did not look for a market very well
* did not able to explain the product in simple terms
* did not try to sell the product, I've just build it
* kept 600 people waiting for a demo while having a product
* should have integrated payment gateway much more earlier
* Facebook & Twitter do not have quality content


**I am a fool. A big one.**

全文完。
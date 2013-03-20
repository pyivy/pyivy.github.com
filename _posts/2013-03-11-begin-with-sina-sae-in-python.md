---
layout: post
title: "新浪 SAE Python 开发入门"
description: "新浪 SAE Python 开发入门"
category: sae
tags: [sae, sina]
---
{% include JB/setup %}

Python 是一门伟大的语言，Django 是一个杰出的框架，SAE 是非常优秀的环境，可惜我的代码写得不太好，文章也一般。

[开发手册](http://sae.sina.com.cn/?m=devcenter&catId=304)

[官方教程 Part 1](https://docs.djangoproject.com/en/1.4/intro/tutorial01/)
[官方教程 Part 2](https://docs.djangoproject.com/en/1.4/intro/tutorial02/)
[官方教程 Part 3](https://docs.djangoproject.com/en/1.4/intro/tutorial03/)
[官方教程 Part 4](https://docs.djangoproject.com/en/1.4/intro/tutorial04/)

### Hello World

新建 Python 应用之后，会有默认的 inddex.wsgi。

{% highlight python%}
#coding:utf8

import sae
import time

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)
    now = time.ctime()
    html_start = '''
    <html>
    <title>Hello Python</title>
    <body>
    <strong>Welcome to SAE</strong> 
    <hr>
    <p>
    '''
    html_end = '''
    <br/><br/>
    By 陈自新.
    </p>
    </body>
    </html>
    '''
    
    return [html_start, now, html_end]

application = sae.create_wsgi_app(app)
{% endhighlight%}

以上作了简单修改，打印当前时间。

### Hello Django

将前例代码 check 到本地：

`$ svn co https://svn.sinaapp.com/olservice`

`$ cd olservice`

`$ django-admin.py startproject olservice`

将 olservice 目录下的所有文件拷贝到 1

`$ rm -rf olservice`

`$ cd 1`

`$ vim config.yaml`

添加以下内容：

{% highlight tex%}
libraries:
- name: "django"
  version: "1.4"
{% endhighlight%}
  
`$ vim index.wsgi`

写入以下内容：

{% highlight python%}
#coding:utf8

import sae
from olservice import wsgi

application = sae.create_wsgi_app(wsgi.application)
{% endhighlight%}

`$ svn add *`

`$ svn ci -m 'add django support'`

访问 [http://olservice.sinaapp.com/](http://olservice.sinaapp.com/)

可见 django 欢迎页面。

>It worked!

>Congratulations on your first Django-powered page.

>Of course, you haven't actually done any work yet. Here's what to do next:

>● If you plan to use a database, edit the DATABASES setting in olservice/settings.py.

>● Start your first app by running python manage.py startapp \[appname].

>You're seeing this message because you have DEBUG = True in your Django settings file and you haven't configured any URLs. Get to work!

### Working with Database

测试本地环境：

`$ python`

{% highlight python%}
>>> import django
>>> help(django)

Help on package django:

NAME
    django

FILE
    /Library/Python/2.7/site-packages/Django-1.4.3-py2.7.egg/django/__init__.py

PACKAGE CONTENTS
    bin (package)
    conf (package)
    contrib (package)
    core (package)
    db (package)
    dispatch (package)
    forms (package)
    http (package)
    middleware (package)
    shortcuts (package)
    template (package)
    templatetags (package)
    test (package)
    utils (package)
    views (package)

FUNCTIONS
    get_version(version=None)
        Derives a PEP386-compliant version number from VERSION.

DATA
    VERSION = (1, 4, 3, 'final', 0)

{% endhighlight%}

线上线下环境一致。

本地调试：

`$ python manage.py runserver 3000`

Database setup

编辑 edit olservice/settings.py.

以下数据库可选：

* django.db.backends.postgresql_psycopg2
* django.db.backends.mysql
* django.db.backends.sqlite3
* django.db.backends.oracle

这里选 django.db.backends.mysql

代码片断：

{% highlight python%}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'olservice', 
        'USER': 'root', 
        'PASSWORD': 'my-pass-word',
        'HOST': '127.0.0.1', 
        'PORT': '3306', 
     }
}
{% endhighlight%}

创建数据库：

`CREATE DATABASE olservice;`

修改[TIME_ZONE](http://en.wikipedia.org/wiki/List_of_tz_zones_by_name)：

`TIME_ZONE = 'Asia/Shanghai'`

修改 [LANGUAGE_CODE](http://www.i18nguy.com/unicode/language-identifiers.html)：

`LANGUAGE_CODE = 'zh-cn'`

By default, INSTALLED_APPS contains the following apps, all of which come with Django:

* django.contrib.auth – An authentication system.
* django.contrib.contenttypes – A framework for content types.
* django.contrib.sessions – A session framework.
* django.contrib.sites – A framework for managing multiple sites with one Django installation.
* django.contrib.messages – A messaging framework.
* django.contrib.staticfiles – A framework for managing static files.

These applications are included by default as a convenience for the common case.

创建这些公用框架的数据库：

`$ python manage.py syncdb`

{% highlight tex%}
reating tables ...
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_user_permissions
Creating table auth_user_groups
Creating table auth_user
Creating table django_content_type
Creating table django_session
Creating table django_site

You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): yes
Username (leave blank to use 'christen'): 
E-mail address: 84856@163.com
Password: # zol#sae
Password (again): 
Superuser created successfully.
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)
{% endhighlight%}

用 phpMyAdmin 查看新建的数据库：

![默认数据库](/assets/images/2013/01/django-data-1.png)

### Creating Models

>Projects vs. apps
>>What’s the difference between a project and an app? An app is a Web application that does something – e.g., a Weblog system, a database of public records or a simple poll app. A project is a collection of configuration and apps for a particular Web site. A project can contain multiple apps. An app can be in multiple projects.

新建一个应用：

`$ python manage.py startapp polls`

新的目录结构：

{% highlight tex%}
polls/
    __init__.py
    models.py
    tests.py
    views.py
{% endhighlight%}

In our simple poll app, we’ll create two models: polls and choices. A poll has a question and a publication date. A choice has two fields: the text of the choice and a vote tally. Each choice is associated with a poll.

{% highlight python%}
from django.db import models

# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
{% endhighlight %}


### Activating Models

修改 settings.py 添加新增的应用：

{% highlight python %}
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'polls',
)
{% endhighlight %}

生成 SQL：

`$ python manage.py sql polls`


{% highlight sql %}
BEGIN;
CREATE TABLE "polls_poll" (
    "id" serial NOT NULL PRIMARY KEY,
    "question" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
CREATE TABLE "polls_choice" (
    "id" serial NOT NULL PRIMARY KEY,
    "poll_id" integer NOT NULL REFERENCES "polls_poll" ("id") DEFERRABLE INITIALLY DEFERRED,
    "choice" varchar(200) NOT NULL,
    "votes" integer NOT NULL
);
COMMIT;
{% endhighlight %}


再次同步数据库，为应用建表。

### Playing with the API

与 Django 对话：

`$ python manage.py shell`

测试 database API

{% highlight python %}
from polls.models import Poll, Choice
Poll.objects.all() # []
from django.utils import timezone
p = Poll(question="What's new?", pub_date=timezone.now())
p.save()
p.id # 1L
p.question = "What's up?"
p.save()
Poll.objects.all() # [<Poll: Poll object>]
{% endhighlight %}

### Activate the Admin Site

修改 olservice/urls.py

打开注释：

{% highlight python %}
from django.contrib import admin
admin.autodiscover()

url(r'^admin/', include(admin.site.urls)),
{% endhighlight %}

测试应用：

`$ python manage.py runserver 3000`

访问：

[http://localhost:3000/admin/](http://localhost:3000/admin/)

### Register Poll in thd Admin

在 polls 目录下创建  admin.py

`$ touch admin.py`

{% highlight python %}
from polls.models import Poll
from django.contrib import admin

admin.site.register(Poll) 
{% endhighlight %}

再次访问应用，可对 Poll 进行 CRUD 。

官方教程中还有进一步的优化指导：

[自定义管理表单](https://docs.djangoproject.com/en/1.4/intro/tutorial02/#customize-the-admin-form)

[添加关联对象](https://docs.djangoproject.com/en/1.4/intro/tutorial02/#adding-related-objects)

### Design your URLs

编辑 olservice/urls.py

{% highlight python %}
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'olservice.views.home', name='home'),
    # url(r'^olservice/', include('olservice.foo.urls')),

    url(r'^polls/$', 'polls.views.index'),
    url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),
    # url(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    # url(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
{% endhighlight %}

### Write your first view

现在开始编写视图。

启动应用，访问 [http://localhost:3001/polls/](http://localhost:3001/polls/)

视图不存在的报错：

{% highlight tex %}
Request Method:	GET
Request URL:	http://localhost:3001/polls/1/
Django Version:	1.4.3
Exception Type:	ViewDoesNotExist
{% endhighlight %}

技巧：配置 URL 访问 docs ，开发过程的得力帮助。

Django 的文档很给力，只要你能沉住气，认真的读，不会有太大的障碍。

注：开发过程中，本地测试访问文档，一切正常，上传到 SAE 之后，因为未安装 [docutils](http://docutils.sf.net/)，无法访问。

第一个视图，纯演示：

编辑 polls/views.py

{% highlight python %}
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")
    
def detail(request, poll_id):
    return HttpResponse("You're looking at poll %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)
{% endhighlight %}

未实现任何数据逻辑，但结构清晰，目测比 Java 的 MVC 容易很多。

[官方文档](https://docs.djangoproject.com/en/1.4/intro/tutorial03/#write-views-that-actually-do-something)详细的介绍了如何真实 View 的编写，并使用了简单的模版。

### Raising 404 and 500

detail 方法用来展示 Poll，有过 Java 编程基础的人，不用理会文档的理论说明部分，直接看代码，很好理解。

{% highlight python %}
from django.http import Http404
# ...
def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('polls/detail.html', {'poll': p})
{% endhighlight %}

Python 的异常处理，利益于语法的优势，非常干净。

详细请看[这里](https://docs.djangoproject.com/en/1.4/intro/tutorial03/#raising-404)。

Django 还为懒汉准备了 `get_object_or_404` 的快捷方法。

404 和 500 错误，也需要自己的视图，依照约定，在 templates 目录下 创建 404.html 和 500.html 即可，可 **借鉴** Google 的样式，简单大方。

### Simplifying the URLconfs

[简化 URL 配置](https://docs.djangoproject.com/en/1.4/intro/tutorial03/#simplifying-the-urlconfs) 这一节，将各个不同模块的 URL 配置分开管理，这不仅仅是一种简化，随着项目的扩张，还有助日后的维护。

项目进行到这里，接下来看教程的[第四部分](https://docs.djangoproject.com/en/1.4/intro/tutorial04/)，最后一步了，实现 `在线投票` 和 `结果展示`。

本地调试正常之后，就可以上传到 SAE了，官方建议开发者使用 [SaeMySQL](http://apidoc.sinaapp.com/sae/SaeMysql.html) 操作数据库。

常量如下：

{% highlight tex%}
用户名　 :  SAE_MYSQL_USER
密　　码 :  SAE_MYSQL_PASS
主库域名 :  SAE_MYSQL_HOST_M
从库域名 :  SAE_MYSQL_HOST_S
端　　口 :  SAE_MYSQL_PORT
数据库名 :  SAE_MYSQL_DB
{% endhighlight%}

修发配置文件：

{% highlight python%}
import sae.const

sae.const.MYSQL_DB      # 数据库名
sae.const.MYSQL_USER    # 用户名
sae.const.MYSQL_PASS    # 密码
sae.const.MYSQL_HOST    # 主库域名（可读写）
sae.const.MYSQL_PORT    # 端口，类型为，请根据框架要求自行转换为int
sae.const.MYSQL_HOST_S  # 从库域名（只读）
{% endhighlight%}

通过 phpMyAdmin 将本地数据导入到线上，测试就用。

可能出现的问题：

**管理后台无样式**

解决方法：

在根目录下添加 

* static/admin/css
* static/admin/img
* static/admin/js 

文件可以 django 的压缩包中找到。

至此，一个粗糙的 SAE Django 应用就跑起来了，当然，外观很魔兽，如果你够执著，可用 [Twitter Bootstrap](http://twitter.github.com/bootstrap/) 美化一下。

为了让页面看起来更加专业，写起来更容易维护，你也需要学习 Django 的模版知识。

限于篇幅，这两个话题，我会另起文章 [Django 开发入门 搭建环境](http://www.pyivy.com/django/2013/03/11/django-a-blog-in-10-min/) 。

全文完。


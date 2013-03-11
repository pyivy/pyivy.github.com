---
layout: post
title: "新浪 SAE Python 开发入门 TBC"
description: "新浪 SAE Python 开发入门"
category: sae
tags: [sae, sina]
---
{% include JB/setup %}

[http://sae.sina.com.cn/?m=devcenter&catId=289](http://sae.sina.com.cn/?m=devcenter&catId=289)

建议开发者使用 [SaeMySQL](http://apidoc.sinaapp.com/sae/SaeMysql.html) 操作数据库。

如果您想自己实现数据库相关操作，可以使用以下常量：

{% highlight tex%}
用户名　 :  SAE_MYSQL_USER
密　　码 :  SAE_MYSQL_PASS
主库域名 :  SAE_MYSQL_HOST_M
从库域名 :  SAE_MYSQL_HOST_S
端　　口 :  SAE_MYSQL_PORT
数据库名 :  SAE_MYSQL_DB
{% endhighlight%}

{% highlight python%}
import sae.const

sae.const.MYSQL_DB      # 数据库名
sae.const.MYSQL_USER    # 用户名
sae.const.MYSQL_PASS    # 密码
sae.const.MYSQL_HOST    # 主库域名（可读写）
sae.const.MYSQL_PORT    # 端口，类型为，请根据框架要求自行转换为int
sae.const.MYSQL_HOST_S  # 从库域名（只读）
{% endhighlight%}

在管理界面创建数据表，默认字符集为utf8，也可设为其他编码。 如果在本地开发环境建立的数据表，请确保使用utf8。在管理界面导入本地数据库时， 也可完成字符集的转换。

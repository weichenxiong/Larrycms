## 介绍：LarryCMS管理系统



## 1.主要功能：

​	。基于django2.2 + mqsql 开发

​	。支持whoosh全文检索。

​	。支持导出Excel文档。

​	。支持数据批量删除，指定数据删除

​	。基于rbac的权限管理系统。 

## 2.安装与启动项目

### 2.1 pip安装： 

`pip install -r requirements.txt`

### 2.2 修改配置

linux下配置都是在settings中的dev文件中，配置文件修改如下：

​		数据库创建：create  database charset=utf8mb4

​		数据库配置如下：

			  DATABASES = {
	"default": {
	    "ENGINE": "django.db.backends.mysql",
	    "HOST": "127.0.0.1",
	    "PORT": 3306,
	    "USER": "root",
	    "PASSWORD": "123",
	    "NAME": "LarryCMS",
	}
	}
### 2.3 数据库迁移

```python
python manage.py makemigrations
python manage.py migrate
```

### 2.4 创建超级用户

```
python manage.py createsuperuser
```

### 2.5 登录admin管理系统，进行路由权限分配

```
权限信息中添加路由，例如：
/users/index/
```

### 2.6 项目运行

```
python manage.py runserver 127.0.0.1:8000
```



## 3.相关问题

有任何问题欢迎加QQ1980575315 进行交流沟通。
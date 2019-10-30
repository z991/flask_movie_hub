# flask_movie_hub
####一.基本功能

```
1.左侧菜单分为两部分，一个是正在热映模块，另外一个是猫眼top模块
2.正在热映页面的数据是实时抓取猫眼电影手机网站的数据，并没有把数据保存到数据库中
3.猫眼top100页面的数据是从数据库中获取的，是先从猫眼电影网站上爬的然后保存到了数据库中。
4.猫眼top100页面支持搜索和排序功能，可以根据电影名称模糊搜索，电影评分高低进行排序
```

#### 二.项目实现思路

```
这次写的项目比较简单，主要是查找功能，重点解决的是数据的获取和数据的展示，因为猫眼电影的数据比豆瓣好爬，就选了猫眼电影作为数据源。模板是从bootstrp上扒的。
```

#### 三、技巧

```
1.这次页面是从bootstrp的起步中找的，使用googel浏览器找到合适的模板右击检查，在Elements中可以修改页面元素，把不要的地方可以删除，认为页面合适就可以右击选择存储，浏览器就会把这个页面的html文件、js文件、css文件等都会下载下来，就免得自己写很多前端代码了。
2.html页面会有复用的地方，所以我把页面html文件拆成了几个部分，导航栏，菜单栏，基本模板等，使用模板的继承或者包含，可以省很多代码，而且维护很方便。
```

uwsgi文件配置

```
[uwsgi]
master = true
chdir = /root/pro/flask_movie_hub/
wsgi-file = /root/pro/flask_movie_hub/manage.py
callable = app
socket = :5000
processes = 4
threads = 2
buffer-size = 32768
daemonize = /root/log/uwsgi.log
```

nginx文件配置

```
user  root;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;
    server {
    listen 8008;
    server_name 13.113.22.155;
          location / {
             include uwsgi_params;
             uwsgi_pass 127.0.0.1:5000;
          }
          location /static {
              alias /root/pro/flask_movie_hub/app/static;
          }
}
}
```


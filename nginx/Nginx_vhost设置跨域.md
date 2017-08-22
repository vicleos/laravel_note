####如何设置nginx vhost xxx.conf 某域名跨域
- 以下是 laravel 为例：
```bash
server
    {
        listen 80;
        #listen [::]:80;
        server_name xxx.xxxx.com;
        index index.html index.htm index.php default.html default.htm default.php;
        root  /mnt/data/wwwroot/xxx;

        include none.conf;
        #error_page   404   /404.html;
        include enable-php.conf;

        try_files $uri $uri/ @rewrite;
        location @rewrite {
            rewrite ^/(.*)$ /index.php?_url=/$1;
        }
        
        # 设置跨域相关头信息
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Headers X-Requested-With;
        add_header Access-Control-Allow-Methods GET,POST,OPTIONS;
        # end
        
        location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
        {
            expires      30d;
        }

        location ~ .*\.(js|css)?$
        {
            expires      12h;
        }

        location ~ /\.
        {
            deny all;
        }

        access_log  /home/wwwlogs/xxx.xxxx.com.log;
    }
```

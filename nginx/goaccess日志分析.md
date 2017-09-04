- https://codeplea.com/goaccess-php

GoAccess is an excellent open source web log analyzer. It makes nice, fancy charts and such:

Screenshot of GoAccess output
GoAccess has several modes of running, including outputting HTML, or severing HTML live with its built-in webserver. I knew I wanted to use GoAccess to analyze my server logs, but I wasn't sure what the best way to use it was.

The built-in webserver has the advantage of always being up-to-date. It has several drawbacks though. Getting it configured to start with the server would be a pain. Keeping it running for each of my sites on different ports would be a mess. Although it does support HTTPS, having it locate my certs would be even more hassle. Finally, I don't know if it can be password protected or not. I could work around a lot of that with a reverse proxy, but then that's a pain to setup and maintain too.

I like easy and simple things. I don't like to setup complicated solutions, because they usually end up being fragile and requiring more maintenance.

So I was looking at having GoAccess run from a cron job, creating a new HTML report every day, and having my webserver serve that. The biggest issues with this is that it'll always be a bit outdated. Even if I run the cron job every hour, it still won't have that "live" feel that I want.

My final solution, I think is a good one. I decided to have GoAccess run from a PHP script on demand. I already have PHP installed, it already runs with HTTPS as I want, and it's trivial to add password protection to a PHP page.

It turns out that having PHP call GoAccess and display the HTML output is simple.
```php
<?php
$output = shell_exec('zcat -f /var/PATH/TO/ACCESS.LOG* | goaccess -a');
echo "$output";
?>
```
The zcat part is so that GoAccess will look at the older rotated logs too, not just the most recent one.

That's really all it takes! Super simple, not much to go wrong, and all I have to do is visit that page to get current analytics. For me, this was the best way to use GoAccess with the least amount of hassle.


#### 日志处理
 * 使用系统自带的 `logrotate` 将 nginx 日志按天分割为并归藏存储
 * `logrotate` 配置文件地址 `/etc/logrotate.conf` 
 * `nginx`日志分割配置文件地址 `/etc/logrotate.d/nginx`
 * 日志默认存放位置：`/data/wwwlogs/`
 * `logrotate`已配置好，日志必须以`****.nginx.log`格式命名，否则不能自动分割
 * `logrotate`已经在 `/etc/cron.daily/logrotate` 配置好自动执行了，但很奇怪的是为什么是在每天3点执行？

`logrotate nginx` 配置文件内容

```
/data/wwwlogs/*nginx.log {
  daily
  rotate 36500
  missingok
  dateext
  compress
  notifempty
  sharedscripts
  postrotate
    [ -e /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
  endscript
}
```

 * 使用 `goAccess` 分析 `nginx` 日志
 
`goAccess` 工具安装配置 https://goaccess.io/

`goAccess`自动分析脚本
```
#!/bin/bash

# 文件作用
# 用goAccess按站点、按周期（天、月）分析日志，将生成 html 文件，保存至 storage 目录
# 注意：文件存在才会执行分析

# 请先创建好目录
# /storage/nginx
# /storage/nginx/web
# /storage/nginx/wap
# /storage/nginx/api

LOG_PATH="/data/wwwlogs"
SAVE_PATH="/data/wwwroot/xxxx/storage/nginx"
LOG_DATE=`date +%Y%m%d`
FILE_DATE=`date -d -1day +%Y%m%d`

#################### 按天分析日志
# Web日志
WEB_DAY_LOG="${LOG_PATH}/www.xxx.com.nginx.log-${LOG_DATE}.gz"
if [ -e ${WEB_DAY_LOG} ]; then
    zcat ${WEB_DAY_LOG} | /usr/local/bin/goaccess - > ${SAVE_PATH}/web/${FILE_DATE}.html
fi

# Wap日志
WAP_DAY_LOG="${LOG_PATH}/m.xxx.com.nginx.log-${LOG_DATE}.gz"
if [ -e ${WAP_DAY_LOG} ]; then
    zcat ${WAP_DAY_LOG} | /usr/local/bin/goaccess - > ${SAVE_PATH}/wap/${FILE_DATE}.html
fi

# Api日志
API_DAY_LOG="${LOG_PATH}/api.xxx.com.nginx.log-${LOG_DATE}.gz"
if [ -e ${API_DAY_LOG} ]; then
    zcat ${API_DAY_LOG} | /usr/local/bin/goaccess - > ${SAVE_PATH}/api/${FILE_DATE}.html
fi

################### 按月分析日志
ISMONTH=`date +%-d`
MONTH=`date -d -1day +%Y%m`
if [ ${ISMONTH} = 1 ]; then
    # Web日志
    zcat ${LOG_PATH}/www.xxx.com.nginx.log-${MONTH}*.gz | /usr/local/bin/goaccess -a > ${SAVE_PATH}/web/${MONTH}.html

    # Wap日志
    zcat ${LOG_PATH}/wap.xxx.com.nginx.log-${MONTH}*.gz | /usr/local/bin/goaccess -a > ${SAVE_PATH}/wap/${MONTH}.html

    # Api日志
    zcat ${LOG_PATH}/api.xxx.com.nginx.log-${MONTH}*.gz | /usr/local/bin/goaccess -a > ${SAVE_PATH}/api/${MONTH}.html

################### 修改日志权限
chown -R www.www ${SAVE_PATH}

```

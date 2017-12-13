#### PHP 区分测试环境 生产环境的方法 环境变量
- Apache Directory 指令中加入 SetEnv RUN_ENV dev , 如下：
```xml
<VirtualHost to.com>
<Directory "/xxx/xxx">
Options FollowSymLinks Indexes
AllowOverride All
Order deny,allow
allow from All
</Directory>
ServerName to.com
ServerAlias to.com
...
SetEnv RUN_ENV dev
</VirtualHost>
```

- 在PHP中可做如下设置：
```php
// 定义运行环境
define('RUN_ENV', isset($_SERVER['RUN_ENV']) ? $_SERVER['RUN_ENV'] : 'production');

require_once DIR_ROOT . '/system/config/' . RUN_ENV . '/config.php';

// 还可以使用 getenv('RUN_ENV') 这种方式来获取环境变量, 如果不存在该环境变量，则为 false
$env = getenv('RUN_MODE');
```

- nginx 如下：
```
fastcgi_param RUNTIME_ENVIROMENT 'DEV'
```

- 查看是否生效，可以 ` echo phpinfo(); ` 来看，Apache 的在 Apache Environment 那块, 其实可以直接 ctrl + f 搜索 `RUN_ENV`

#### 参考链接:
- http://blog.csdn.net/default7/article/details/49329585
- https://stackoverflow.com/questions/5448943/setenv-application-env-development-htaccess-interacting-with-zend-framework
- https://www.cnblogs.com/debmzhang/p/3374674.html
- http://php.net/manual/zh/function.getenv.php

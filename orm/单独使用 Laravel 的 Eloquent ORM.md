Laravel 的 Eloquent ORM非常简洁优雅，我想在自己的项目中使用可以么？

答案是可以的。下面我们来讲下

Laravel ORM 用的是 Illuminate Database 开源的库

github地址：

https://github.com/illuminate/database

Composer安装方法：

composer require illuminate/database

composer require illuminate/events

安装好后就可以使用了。

#### 在你的公共文件或入口文件创建一个新的“Capsule”管理器实例
```php
use Illuminate\Database\Capsule\Manager as Capsule;

// Autoload 自动载入

require '../vendor/autoload.php';

// Eloquent ORM

$capsule = new Capsule;

$capsule->addConnection(require '../config/database.php');

$capsule->bootEloquent();

// 路由配置

require '../config/routes.php';
```
#### 新增 config/database.php （注意替换数据库密码）：
```php
<?php

return [

  'driver'    => 'mysql',

  'host'      => 'localhost',

  'database'  => 'test',

  'username'  => 'root',

  'password'  => '123456',

  'charset'   => 'utf8',

  'collation' => 'utf8_general_ci',

  'prefix'    => ''

  ];
```
#### 修改 models/Article.php ：
```php
<?php

/**

* Article Model

*/

class Article extends Illuminate\Database\Eloquent\Model

{

  public $timestamps = false;

}
```

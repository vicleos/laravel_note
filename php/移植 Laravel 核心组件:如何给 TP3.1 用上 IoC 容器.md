ThinkPHP引入IoC , 需要几步呢?如下:
```
1. 确保ThinkPHP 3.1 项目运行在 php 5.4 以上环境中
2. 给ThinkPHP 3.1 引入Composer
3. 独立出Laravel的Container组件
4. 为扩展功能设计架构
5. 创建引入ThinkPHP的引导文件
```
一. 给ThinkPHP 3.1 引入Composer
时至今日 , ThinkPHP自身的autoload管理功能已经非常老旧了 , 有这几个关键的痛点:
```
没有命名空间,大量关键类同名
引入外部库还要用令人费解的import()方法
生成autoload的代码位置 , 在设计理念上有错
靠ThinkPHP去管理各种现代依赖 , 基本是不可能完成的任务 . 这时Composer就大显身手了.
```
我们可以在任意文件夹创建 Composer.json 文件 , 然后按自己的设想任意构建扩展. 运行composer install指令后,composer就自动为我们下载了所有依赖,并生成了 vendor/autoload.php 文件.

瞥一眼vendor/autoload.php 文件,会发现它其实就干了两件事 :
```
引入了 vendor/composer/ClassLoader.php,这里注册了各种 Autoload 机制的引用文件方法
引入了按composer.json文件定义的classmap,files,psr-0,psr-4等规范 , 生成的类名路径映射关系文件.
```
所以我们只要把 vendor/autoload.php 在ThinkPHP项目中require 进来, 就可以随心所欲使用任何自定义类和扩展,再不要受TP3.1规范的约束了.

问题是autoload.php要在哪里引入比较合适呢? 经过反复测试,还是在Public/index.php 中引入较好:
```php
/**
 * 系统调试设置
 * 项目正式部署后请设置为false
 */
define ( 'APP_DEBUG', true );
define ( 'APP_PATH', realpath(dirname(__FILE__) ."/../") ."/" );
define ( 'WEB_PATH', realpath(dirname(__FILE__)) ."/" );
/**
 * 引入核心入口
 * ThinkPHP亦可移动到WEB以外的目录
 */

//------------!!!在这里引入Composer的autoload!!------------//
require '../../Extends/vendor/autoload.php';
require '../ThinkPHP/ThinkPHP.php';
```
这是因为ThinkPHP有非常糟糕的引导机制:
```
index.php  --require--> ThinkPHP.php --require--> Common/runtime.php
```
这个过程是单线的,穿插大量必要的宏定义,和大量的if逻辑. 最关键的启动代码 Think::Start(); 却在 runtime.php 最后一行执行.

这好比把衣服裤子鞋子做成了一件连体服.想要加一根腰带,要么脱光,要么剪开衣服.与其在劈头盖脸的if else中找剪裁点,还是选择脱光吧.

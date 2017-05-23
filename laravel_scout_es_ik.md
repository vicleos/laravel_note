#使用 Laravel Scout，Elasticsearch，ik 分词
利用上述组建自己的搜索框架

# 第一步.linux安装jdk8


```
sudo apt-get install openjdk-8-jre
```
- 参考：http://openjdk.java.net/install/index.html


# 第二步.安装 ElasticSearch Scout Engine 包


注意：如果是 `laravel 5.3` 则使用：
```
composer require tamayo/laravel-scout-elastic:2.0.0
```

`laravel 5.4` 直接使用：

```
composer require tamayo/laravel-scout-elastic
```

安装这个包的时候，顺便就会装好 Laravel Scout，我们 publish 一下 config

```
$ php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

添加对应的 ServiceProvider:

具体位置在 `/config/app.php` 中的 `providers` 数组中

```
...
Laravel\Scout\ScoutServiceProvider::class,
ScoutEngines\Elasticsearch\ElasticsearchProvider::class

```
# 第三步：安装 ElasticSearch



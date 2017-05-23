#使用 Laravel Scout，Elasticsearch，ik 分词组建自己的搜索框架
### 必要条件：
```
a.JDK8+  
b.系统可用内存>2G 
```
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

因为我们要使用 ik 插件，在安装这个插件的时候，如果自己想办法安装这个插件会浪费你很多精力。

所以我们直接使用项目： https://github.com/medcl/elasticsearch-rtf

当前的版本是 Elasticsearch 5.1.1，ik 插件也是直接自带了。

安装好 ElasticSearch，跑起来服务，测试服务安装是否正确：

```
$ curl http://localhost:9200
```
```
{
  "name" : "Rkx3vzo",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "Ww9KIfqSRA-9qnmj1TcnHQ",
  "version" : {
    "number" : "5.1.1",
    "build_hash" : "5395e21",
    "build_date" : "2016-12-06T12:36:15.409Z",
    "build_snapshot" : false,
    "lucene_version" : "6.3.0"
  },
  "tagline" : "You Know, for Search"
}
```
如果正确的打印以上信息，证明 ElasticSearch 已经安装好了。

接着你需要查看一下 ik 插件是否安装（请在你的 ElasticSearch 文件夹中执行）：
```
$ ./bin/elasticsearch-plugin list
analysis-ik
```
如果出现 analysis-ik，证明 ik 已经安装。

# 配置 `config/scout.php` 参数信息

```
...
  'driver' => env('SCOUT_DRIVER', 'elasticsearch'),
...
  'elasticsearch' => [
      'index' => env('ELASTICSEARCH_INDEX', 'jkg'),
      'config' => [
          'hosts' => [
              //如果在服务端 Es 启用了 sheild 验证，需要填写认证信息(默认用户名 elastic 密码 changeme )
              //参考：https://www.elastic.co/guide/en/elasticsearch/client/php-api/master/_security.html
              //env('ELASTICSEARCH_HOST', 'http://elastic:changeme@127.0.0.1'),
              //没开启 sheild 验证，则只填写服务端 Es 地址即可
              env('ELASTICSEARCH_HOST', 'http://127.0.0.1'),
          ],
      ]
  ],
```

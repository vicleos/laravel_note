#使用 Laravel Scout，Elasticsearch，ik 分词
利用上述组建自己的搜索框架

##1.linux安装jdk8

```
sudo apt-get install openjdk-8-jre
```

- 参考：http://openjdk.java.net/install/index.html

##2.安装 ElasticSearch Scout Engine 包
注意：如果是 `laravel 5.3` 则使用：

```
composer require tamayo/laravel-scout-elastic:2.0.0
```

`laravel 5.4` 直接使用：

```
composer require tamayo/laravel-scout-elastic
```


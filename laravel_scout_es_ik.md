#使用 Laravel Scout，Elasticsearch，ik 分词组建自己的搜索框架
### 必要条件：
```
a.JDK8+  
b.系统可用内存>2G 
```
# 第一步.linux安装jdk8


```bash
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

```bash
$ php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

添加对应的 ServiceProvider:

具体位置在 `/config/app.php` 中的 `providers` 数组中

```php
...
Laravel\Scout\ScoutServiceProvider::class,
ScoutEngines\Elasticsearch\ElasticsearchProvider::class

```
# 第三步：安装 ElasticSearch

因为我们要使用 ik 插件，在安装这个插件的时候，如果自己想办法安装这个插件会浪费你很多精力。

所以我们直接使用项目： https://github.com/medcl/elasticsearch-rtf

当前的版本是 Elasticsearch 5.1.1，ik 插件也是直接自带了。

安装好 ElasticSearch，跑起来服务，测试服务安装是否正确：

```bash
$ curl http://localhost:9200
```
```bash
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
```bash
$ ./bin/elasticsearch-plugin list
analysis-ik
```
如果出现 analysis-ik，证明 ik 已经安装。

# 配置 `config/scout.php` 参数信息

```php
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

# 客户端初始化 Es 索引和模版参数
### 参考文档：
- 如何创建索引：https://www.elastic.co/guide/cn/elasticsearch/guide/current/_creating_an_index.html
- 索引模版：https://www.elastic.co/guide/cn/elasticsearch/guide/current/index-templates.html

创建新的命令行用来执行初始化

```bash
$ php artisan make:command InitHelloEs
```
修改生成的命令行类
```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
//使用 GuzzleHttp 请求组件
use GuzzleHttp\Client;

class InitHelloEs extends Command
{
    /**
     * The name and signature of the console command.
     *
     */
    protected $signature = 'es:init';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Init es to create index';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $client = new Client();
        $this->createTemplate($client);
        $this->createIndex($client);
    }

    protected function createIndex(Client $client)
    {
        var_dump('do createIndex');
        var_dump(config('scout.elasticsearch.config.hosts'))[0];
        $url = config('scout.elasticsearch.config.hosts')[0] . ':9200/' . config('scout.elasticsearch.index');
        $client->put($url, [
            'json' => [
                'settings' => [
                    'refresh_interval' => '5s',
                    'number_of_shards' => 1,
                    'number_of_replicas' => 0,
                ],
                'mappings' => [
                    '_default_' => [
                        '_all' => [
                            'enabled' => false
                        ]
                    ]
                ]
            ]
        ]);
    }

    protected function createTemplate(Client $client)
    {
        var_dump('do createTemplate');
        var_dump(config('scout.elasticsearch.config.hosts'));
        $url = config('scout.elasticsearch.config.hosts')[0] . ':9200/' . '_template/rtf';
        $rst = $client->put($url, [
            'json' => [
                'template' => '*',
                'settings' => [
                    'number_of_shards' => 1
                ],
                'mappings' => [
                    '_default_' => [
                        '_all' => [
                            'enabled' => true
                        ],
                        'dynamic_templates' => [
                            [
                                'strings' => [
                                    'match_mapping_type' => 'string',
                                    'mapping' => [
                                        'type' => 'text',
                                        'analyzer' => 'ik_smart',
                                        'ignore_above' => 256,
                                        'fields' => [
                                            'keyword' => [
                                                'type' => 'keyword'
                                            ]
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]);
        var_dump($rst);
    }
}

```
# 在 Model 中启用 Es 搜索

```php
...
use Laravel\Scout\Searchable;

class Article extends Model
{
  ...
  use Searchable;
  ...
  /**
   * es 搜索方法
   * @return [type] [description]
   */
  public function toSearchableArray()
  {
      //对应的字段
      return [
          'intro' => $this->intro
      ];
  }
}
```




#### PHP底层和mysql的通信原理

需要清楚的几个概念：

FPM 进程：进程数在 ` php-fpm.ini ` 中设置。
没有设置 `max_requests` ，那么进程是不会销毁的。
也就是说当一个进程里面出现死循环或者内存溢出等导致进程僵死的情况出现的时候，处理的进程就会少一个。

mysql 连接数：一个进程连接到 mysql 的一个库，算是一个连接。
连接数默认 100，我们线上是 5000，进程数在 `my.cnf` 中设置。
mysql 连接数要大于等于 FPM 进程数，否则会报错。

长连接和短连接：FPM 短连接 MYSQL 的时候，无需调用 `CLOSE` 函数，因为在 `RSHUTDOWN` 的时候，会调用清理。
长连接的时候，需要调用 close，长连接会一直霸占资源，直到进程死掉。

首先我们来理解一下 `php-fpm` 的工作原理，`php-fpm` 是一个 `php-cgi` 进程管理器，其实就是一个连接池，它和 `nginx` 配合的工作原理如下。

我们先从最简单的静态方式入手观察他的工作原理

```
vim php-fpm.ini
```
```
[www]

pm = static

pm.max_children = 5

pm.max_requests = 2
```
<pre>
上面三句话的含义是什么呢:

1、static 表示静态以静态方式生成 php-fpm 进程

2、pm.max_children = 5 表示当 php-fpm 启动时就启动 5 个 php-fpm 子进程 等待处理 nginx 发过来的请求

3、pm.max_requests = 2 表示每个 php-fpm 子进程处理 2 个请求就销毁，当然父进程每次看到有销毁的自然也就会生成新的子进程

我们来简单验证一下这个说法：

首先重启 php-fpm，让它复位一下

接下来写一条简单的语句输出当前进程ID
</pre>
```php
echo "当前 php-fpm 进程ID：".posix_getpid();
```

不断刷新浏览器观察输出变化

```bash
当前 php-fpm 进程ID：24548

当前 php-fpm 进程ID：24549

当前 php-fpm 进程ID：24550

当前 php-fpm 进程ID：24547

当前 php-fpm 进程ID：24551

....
```
<pre>

可以看得出，第一批id不是按照顺序执行的，进程id为24547的进程是在第四位处理的。
然后从下面开始，所有id都是顺序执行的而且每次生成的一批id都是递增，是不是有种mysql自增主键的赶脚呢？

这里需要注意的是，无论是静态还是下面的动态配置方式，只要没有设置 max_requests ，那么进程是不会销毁的。
也就是说当一个进程里面出现死循环或者内存溢出等导致进程僵死的情况出现的时候，处理的进程就会少一个了

好吧理解了静态的处理方式，我们其实也很容易知道这个方式的弊端了。
当然我们平时服务器不可能就开5个进程每个进程处理2个请求，我们来做一个简单的加减乘除，看看一个服务器应该开多少个 php-fpm 合适

首先我们来看看一个简单的echo需要多少内存：

</pre>
```php

$size = memory_get_usage();

$unit = array('b','kb','mb','gb','tb','pb');

$memory = @round($size/pow(1024,($i=floor(log($size,1024)))),2).' '.$unit[$i];

echo "当前 php-cgi 进程所使用内存：".$memory;

```
<pre>

观察浏览器我们可以得到一下数据：

当前 php-cgi 进程所使用内存：227.17 kb

也就是说一个简单的什么都不干的php就已经占用了200多K的内存，当然这也不算多。

不过进程多了cpu切换进程速度就会变慢，所以这个数还是需要通过ab等测试工具才能测试出具体应该开多少比较合理

我们先从200个cgi进程开始，不断的增加，架设增加到800的时候，效率和400一样，那我们就没必要开800那么多进程浪费内存了。

那么问题就来了，如果同一时间请求出超过400呢？有人说会排队等待，真的会排队等待吗？
答案明显是 php-fpm 是没能力排队了，因为处理请求的php-fpm子进程都用完了，那么等待也就只能是在 nginx 等待。
通常一个 nginx 也不只是转发请求给 php-fpm 就完事了，他还要处理静态文件呢？
如果这些php请求导致nginx的请求数过多一直在等待，那么访问静态文件自然也会卡了，这时候我们就需要配置成下面的动态处理方式。

</pre>
```
[www]

pm.max_children = 10

pm.start_servers = 5

pm.min_spare_servers = 2

pm.max_spare_servers = 8

;pm.max_requests = 2

```
<pre>

上面五句话的含义是什么呢:

1、dynamic 表示静态以动态方式生成 php-fpm 进程

2、pm.max_children = 10 同时活动的进程数 10个

3、pm.start_servers = 5 表示当 php-fpm 主进程启动时就启动 5 个 php-fpm 子进程

4、pm.min_spare_servers = 2 表示最小备用进程数

5、pm.max_spare_servers = 8 表示最大备用进程数

6、pm.max_requests = 2 上面说过就不说了

</pre>
```
当前 php-fpm 进程ID：2270

当前 php-fpm 进程ID：2271

当前 php-fpm 进程ID：2272

....

当前 php-fpm 进程ID：2272

当前 php-fpm 进程ID：2273

当前 php-fpm 进程ID：2274

```
<pre>

为什么这里没有重新生成新的进程？因为pm.max_requests = 2被注释掉了，这个上面其实已经提及过一次了

我们也可以从 ps 看出这批进程id

</pre>

```bash
ps aux|grep php

root 2269 0.0 0.1 134560 4616 ? Ss 14:27 0:00 php-fpm: master process (/etc/php/php-fpm.ini)

www-data 2270 0.2 0.2 136736 9188 ? S 14:27 0:00 php-fpm: pool www

www-data 2271 0.2 0.2 136740 9192 ? S 14:27 0:00 php-fpm: pool www

www-data 2272 0.2 0.2 134684 7284 ? S 14:27 0:00 php-fpm: pool www

www-data 2273 0.2 0.2 136732 9120 ? S 14:27 0:00 php-fpm: pool www

www-data 2274 0.1 0.2 134684 7244 ? S 14:27 0:00 php-fpm: pool www

```
<pre>

从上面我们可以看到一个 id 为 2269 的 php-fpm 主进程 管理着 id 为 2270、2271、2272、2273、2274 的5个php-fpm 子进程

这里需要注意的是，当并发大过start_servers数的处理能力是，备用进程才会启动，当并发数小的时候，备用进程也会销毁掉。
所以无论什么时候，ps 出来的进程都是上面那5个

下面来看看php-fpm+mysql的效果
</pre>

```bash
mysql> show processlist;

+----+------------------+-----------+------+---------+------+----------------+-------------------------+

| Id | User | Host | db | Command | Time | State | Info |

+----+------------------+-----------+------+---------+------+----------------+-------------------------+

| 9 | root | localhost | NULL | Query | 0 | NULL | show processlist |

+----+------------------+-----------+------+---------+------+----------------+-------------------------+
```

接下来我们看短连接：

```php
$conn = new mysqli("192.168.0.170", "redol", "redol", "test_db");
```

然后不断访问上面的php文件，每次看到的都是
```bash
+----+---------+-----------+------+---------+------+----------------+--------------------+

| Id | User | Host | db | Command | Time | State | Info |

+----+---------+-----------+------+---------+------+----------------+--------------------+

| 9 | root | localhost | NULL | Query | 0 | NULL | show processlist |

+----+---------+-----------+------+---------+------+----------------+--------------------+
```

这也是php神奇的地方，居然不用close的，每次请求完了他就自己给你close掉和mysql的连接了，这点确实也让很多新手少了不少下面的烦恼啊

```
Warning: mysqli::mysqli(): (HY000/1040): Too many connections in ...
```

不要以为语言应该都是这样那就打错特错了，去看看golang吧

下面看看长连接
```php
$conn = new mysqli("p:192.168.0.170", "redol", "redol", "test_db");
```

你没看错，mysqli的长连接和mysql不同，是在host前面加 p:，没有mysqli_pconnet 的用法，估计很多刚开始用mysqli也是摸不着头脑吧？

第一次访问：
```bash

+----+-------+-------------------------+-------+---------+------+-------+------------------+

| Id | User | Host | db | Command | Time | State | Info |

+----+-------+-------------------------+-------+---------+------+-------+------------------+

| 9 | root | localhost | NULL | Query | 0 | NULL | show processlist |

| 10 | redol | bbs.demo.kkk5.com:16650 | redol | Sleep | 34 | | NULL |

+----+-------+-------------------------+-------+---------+------+-------+------------------+
```

刷新一下网页
```bash
+-----+-------+-------------------------+-------+---------+------+-------+------------------+

| Id | User | Host | db | Command | Time | State | Info |

+-----+-------+-------------------------+-------+---------+------+-------+------------------+

| 9 | root | localhost | NULL | Query | 0 | NULL | show processlist |

| 10 | redol | bbs.demo.kkk5.com:16650 | redol | Sleep | 4 | | NULL |

| 727 | redol | bbs.demo.kkk5.com:16657 | redol | Sleep | 1 | | NULL |

+-----+-------+-------------------------+-------+---------+------+-------+------------------+
```

再刷新一下网页，效果我就不发了，反正你知道最后无论怎么刷新，都是如下即可
```bash
+-----+-------+-------------------------+-------+---------+------+-------+------------------+

| Id | User | Host | db | Command | Time | State | Info |

+-----+-------+-------------------------+-------+---------+------+-------+------------------+

| 9 | root | localhost | NULL | Query | 0 | NULL | show processlist |

| 10 | redol | bbs.demo.kkk5.com:16650 | redol | Sleep | 4 | | NULL |

| 727 | redol | bbs.demo.kkk5.com:16657 | redol | Sleep | 1 | | NULL |

| 728 | redol | bbs.demo.kkk5.com:16659 | redol | Sleep | 16 | | NULL |

| 729 | redol | bbs.demo.kkk5.com:16661 | redol | Sleep | 12 | | NULL |

| 730 | redol | bbs.demo.kkk5.com:16663 | redol | Sleep | 8 | | NULL |

+-----+-------+-------------------------+-------+---------+------+-------+------------------+
```

也就是说，长连接是真的会一直霸占mysql连接的，那么问题就来了，如果我没有重启 php-fpm，只重启了mysql，会出现什么问题呢？答案是第一次连接的时候会报下面错误
```bash
Warning: mysqli::mysqli(): MySQL server has gone away in    //也就是连接已经存在
```
<pre>
所以用长连接query前还是先判断有没有连接，没有就close连接，注意一定要close，再连接，否则连接是失效的。

下面我们来试试 Too many connections 的错误吧

先调整一下mysql的最大连接数
</pre>
```bash
vim /etc/mysql/my.cnf
```
```
max_connections = 3
```
你没看错，我只给了他3个连接，而上面的php-fpm是5个，所以结果不用我说都知道了吧，如期的出现
```
Warning: mysqli::mysqli(): (HY000/1040): Too many connections in ...
```
<pre>
所以线上的mysql，还是注意一下这个max_connections数吧，我只能告诉你他默认是100，如果你觉得100不够用的话，自己改去吧

从上面可知，短连接是不用close也会自动关闭的。
那如果是设置了 pm.max_requests = 2，每个php-fpm处理两个请求就销毁，销毁了会close么？
我就不截图了，直接告诉答案吧，会的。
所以无论如何，看到的mysql都是1、2、3、4、5、4、3、2、1、2、3、4、5这样的连接数，就是慢慢增加，再慢慢减少。
减少是因为php-fpm子进程销毁了嘛

</pre>

- 参考
- https://www.jianshu.com/p/d955a5413c7e

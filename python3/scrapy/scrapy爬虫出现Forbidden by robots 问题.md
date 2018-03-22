
先说结论，关闭scrapy自带的ROBOTSTXT_OBEY功能，在setting找到这个变量，设置为False即可解决。 

使用scrapy爬取淘宝页面的时候，在提交http请求时出现debug信息Forbidden by robots.txt，看来是请求被拒绝了。

开始以为是淘宝页面有什么保密机制，防止爬虫来抓取页面，于是在spider中填入各种header信息，伪装成浏览器，结果还是不行。。。

用chrome抓包看了半天感觉没有影响简单页面抓取的机制（其他保密机制应该还是有的，打开一个页面时，向不同服务器递交了很多请求，还设定了一些不知道干啥的cookies），

最后用urllib伪造请求发现页面都能抓取回来。

于是上网查了一下robot.txt是什么，发现原来有个robot协议，终于恍然大悟：

我们观察scrapy抓包时的输出就能发现，在请求我们设定的url之前，它会先向服务器根目录请求一个txt文件：
```
2016-06-10 18:16:26 [scrapy] DEBUG: Crawled (200) <GET https://item.taobao.com/robots.txt> (referer: None)
```
这个文件中规定了本站点允许的爬虫机器爬取的范围（比如你不想让百度爬取你的页面，就可以通过robot来限制），因为默认scrapy遵守robot协议，

所以会先请求这个文件查看自己的权限，而我们现在访问这个url得到
```
User-agent: *
Disallow: /
```
可以看见，淘宝disallow根目录以下所有页面。。。。（似乎有新闻说淘宝关闭了爬虫对它们的爬取权限，因为涉及到用户隐私）所以scrapy就停止了之后的请求和页面解析。 

我们在setting改变ROBOTSTXT_OBEY为False，让scrapy不要遵守robot协议，之后就能正常爬取了。


```
2016-06-10 18:27:38 [scrapy] INFO: Spider opened
2016-06-10 18:27:38 [scrapy] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2016-06-10 18:27:38 [scrapy] DEBUG: Crawled (200) <GET https://item.taobao.com/xxxxxxx> (referer: None)
```

对于使用robot协议的站点，只需要我们的爬虫不遵守该协议，就可以了，但是对于防止爬虫爬取，站点还有检查请求头、检查ip等等手段，还需要其他的相应处理。

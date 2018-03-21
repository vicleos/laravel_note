from: https://www.cnblogs.com/kongzhagen/p/6549053.html

#### 创建项目：
```bash
scrapy startproject movie
cd movie
scrapy genspider meiju meijutt.com
```

#### 文件说明：

- scrapy.cfg  项目的配置信息，主要为Scrapy命令行工具提供一个基础的配置信息。（真正爬虫相关的配置信息在settings.py文件中）
- items.py    设置数据存储模板，用于结构化数据，如：Django的Model
- pipelines    数据处理行为，如：一般结构化的数据持久化
- settings.py 配置文件，如：递归的层数、并发数，延迟下载等
- spiders      爬虫目录，如：创建文件，编写爬虫规则

#### 执行爬虫:
```bash
cd movie
scrapy crawl meiju --nolog
```

#### 小问题：
在使用 Visual Studio Code 时，在 items.py 中的 import scrapy 语句，pylint 报出问题 [pylint] E0401:Unable to import 'scrapys'

这应该是应为选择 python 的解析器不对，Ctrl+Shift+P 打开控制台，输入 `>python: s` 在下拉菜单中点击 `Python: Select Interpreter`，

现在显示目前选择的解析器是 `Anaconda3` 的，所以我们改为选择系统的 python3 程序。

然后，就好了

- 参考：https://code.visualstudio.com/docs/python/environments


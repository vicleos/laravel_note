- 当我pip install scrapy过程中发现Twisted报错。

- 于是我尝试pip install twisted单独安装Twisted, 依然是报错。

- 后来发现原来是twisted和高版本的python有兼容性问题。

- 那么怎么解决呢？

- 我发现了Python扩展包的非官方Windows二进制文件里有：
- https://www.lfd.uci.edu/~gohlke/pythonlibs/ 搜索 twisted
- 下载了 Twisted‑17.9.0‑cp36‑cp36m‑win_amd64.whl

- 执行：
```
pip install  Twisted‑17.9.0‑cp36‑cp36m‑win_amd64.whl
```
- 执行：
```
pip install  Twisted‑17.9.0‑cp36‑cp36m‑win32.whl
```
成功了！
```
D:\python>pip install Twisted-17.9.0-cp36-cp36m-win_amd64.whl
Processing d:\python\twisted-17.9.0-cp36-cp36m-win_amd64.whl
Requirement already satisfied: Automat>=0.3.0 in c:\users\xxx\appdata\local\programs\python\python36\lib\site-packages (from Twisted==17.9.0)
Requirement already satisfied: hyperlink>=17.1.1 in c:\users\xxx\appdata\local\programs\python\python36\lib\site-packages (from Twisted==17.9.0)
Requirement already satisfied: incremental>=16.10.1 in c:\users\xxx\appdata\local\programs\python\python36\lib\site-packages (from Twisted==17.9.0)
Requirement already satisfied: constantly>=15.1 in c:\users\xxx\appdata\local\programs\python\python36\lib\site-packages (from Twisted==17.9.0)
Requirement already satisfied: zope.interface>=4.0.2 in c:\users\xxx\appdata\local\programs\python\python36\lib\site-packages (from Twisted==17.9.0)
Requirement already satisfied: six in c:\users\xxx\appdata\roaming\python\python36\site-packages (from Automat>=0.3.0->Twisted==17.9.0)
Requirement already satisfied: attrs in c:\users\xxx\appdata\local\programs\python\python36\lib\site-packages (from Automat>=0.3.0->Twisted==17.9.0)
Requirement already satisfied: idna>=2.5 in c:\users\xxx\appdata\local\programs\python\python36\lib\site-packages (from hyperlink>=17.1.1->Twisted==17.9.0)
Requirement already satisfied: setuptools in c:\users\xxx\appdata\local\programs\python\python36\lib\site-packages (from zope.interface>=4.0.2->Twisted==17.9.0)
Installing collected packages: Twisted
Successfully installed Twisted-17.9.0
```

- 如果在运行的过程中，需要pywin32, 可以使用下面命令安装：pip install pypiwin32

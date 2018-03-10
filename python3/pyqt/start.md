- 完美安装 Anaconda3 + PyQt5 + Eric6 | http://blog.csdn.net/weiaitaowang/article/details/52045360
- 快速熟悉 PyQt5 与 Eric6 的极速 GUI 开发 | http://blog.csdn.net/mengtianwxs/article/details/53406912

> PyQt5: 这里折腾了很久，上面的攻略中用到的Pyqt5.6 exe是适配python3.5的，现在Anaconda已经python3.6了，如果安装这个exe，会导致Anaconda Nevigator 和spyder打不开，经过几番询问度娘和谷哥，发现从Pyqt5.7开始，不会再提供exe的版本，这条路彻底走不通了，可以用下面的方法:

> pip install pyqt5

> pip install pyqt5-tools ：这个装完后把安装路径（例如C:\ProgramData\Anaconda3\Lib\site-packages\pyqt5-tools）下的designer.exe 拷贝到 C:\ProgramData\Anaconda3\Lib\site-packages\PyQt5\Qt\bin，否则Eric6运行的时候会报错，说找不到designer

> pip install qscintilla

- 链接：https://www.jianshu.com/p/4ed9330108e0


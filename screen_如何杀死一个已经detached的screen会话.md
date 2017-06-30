
- 如果想杀死一个已经detached的screen会话，可以使用以下命令：

```bash
   screen -X -S [session # you want to kill] quit
```

- 举例如下：

```bash
[root@localhost ~]# screen -ls
There are screens on:
        9975.pts-0.localhost    (Detached)
        4588.pts-3.localhost    (Detached)
2 Sockets in /var/run/screen/S-root.

[root@localhost ~]# screen -X -S 4588 quit
[root@localhost ~]# screen -ls
There is a screen on:
        9975.pts-0.localhost    (Detached)
1 Socket in /var/run/screen/S-root.
```

- 可以看到，4588会话已经没有了。

参考资料：
- http://stackoverflow.com/questions/1509677/kill-detached-screen-session

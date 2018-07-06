#### 错误信息
```
[ERROR] InnoDB: Attempted to open a previously opened tablespace. Previous tablespace isaactest/wp_usermeta uses space ID: 2 at filepath: .\isaactest\wp_usermeta.ibd. Cannot open tablespace MySQL/innodb_index_stats which uses space ID: 2 at filepath: .\mysql\innodb_index_stats.ibd 
InnoDB: Error: could not open single-table tablespace file .\mysql\innodb_index_stats.ibd 
InnoDB: We do not continue the crash recovery, because the table may become 
InnoDB: corrupt if we cannot apply the log records in the InnoDB log to it. 
InnoDB: To fix the problem and start mysqld: 
InnoDB: 1) If there is a permission problem in the file and mysqld cannot 
InnoDB: open the file, you should modify the permissions. 
InnoDB: 2) If the table is not needed, or you can restore it from a backup, 
InnoDB: then you can remove the .ibd file, and InnoDB will do a normal 
InnoDB: crash recovery and ignore that table. 
InnoDB: 3) If the file system or the disk is broken, and you cannot remove 
InnoDB: the .ibd file, you can set innodb_force_recovery > 0 in my.cnf 
InnoDB: and force InnoDB to continue crash recovery here. 
```

#### 结局方案
```
在 my.cnf 中加入一行
innodb_force_recovery = 1
这时就能启动 mysql 了，启动以后，检查下数据库可以正常打开后，再将这行去掉就可以了
```

#### 参考资料
- http://blog.itpub.net/22664653/viewspace-1441389/
- Mysql innodb_force_recovery参数设置解释 https://blog.csdn.net/vivenwan/article/details/53259516

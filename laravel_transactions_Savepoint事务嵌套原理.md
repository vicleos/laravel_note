- mysql官方并不支持事务嵌套，当第二个事务开始时候，会隐式的先调用commit提交之前的事务，而后在开启第二次的事务。

- 在正常开发中难免会出现失误嵌套的情况。如何解决呢？

- `laravel` 框架使用了 `mysql` 的 `SAVEPOINT` 方法来解决这一问题。

- `mysql savepoint`
- 首先来看下mysql原生案例：

```bash
# 表结构
+----------+------------------+------+-----+---------+----------------+
| Field    | Type             | Null | Key | Default | Extra          |
+----------+------------------+------+-----+---------+----------------+
| id       | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| username | varchar(32)      | NO   |     | NULL    |                |
| password | varchar(32)      | NO   |     | NULL    |                |
+----------+------------------+------+-----+---------+----------------+
```
- 2次开启事务案例 ：
```bash
# 操作
mysql> begin;       # 开启事务
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into user(username, password) values('ff', 'ff');
Query OK, 1 row affected (0.00 sec)
 
mysql> begin;       # 此处mysql会先提交前一个事务，再开启后一个事务。
Query OK, 0 rows affected (0.01 sec)
 
mysql> insert into user(username, password) values('ee', 'ee');
Query OK, 1 row affected (0.00 sec)
 
mysql> rollback;    # 事务回滚，把username=ee回滚掉了，而ff已插入数据库。
Query OK, 0 rows affected (0.00 sec)
```
- savepoint 案例：
```bash
mysql> begin;                   # 开启事务
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into user(username, password) values('ff', 'ff');
Query OK, 1 row affected (0.00 sec)
 
mysql> SAVEPOINT trans_1;       # 创建回滚点trans_1
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into user(username, password) values('ee', 'ee');
Query OK, 1 row affected (0.00 sec)
 
mysql> SAVEPOINT trans_2;       # 创建回滚点trans_2
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into user(username, password) values('gg', 'gg');
Query OK, 1 row affected (0.00 sec)
 
mysql> ROLLBACK TO SAVEPOINT trans_2;   # 回滚到trans_2，将username=gg回滚掉了
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into user(username, password) values('hh', 'hh');
Query OK, 1 row affected (0.00 sec)
 
mysql> commit;                  # 提交数据
Query OK, 0 rows affected (0.00 sec)
```
- ↑ 上面例子中username=gg被回滚掉了，最终数据库中插入了username=ee,ff,hh。如果最后commit换成rollback所有数据将全部回滚。

- laravel 5.3 实现
```php
    /**
     * Start a new database transaction.
     *
     * @return void
     * @throws Exception
     */
    public function beginTransaction()
    {
        if ($this->transactions == 0) {
            try {
                $this->getPdo()->beginTransaction();
            } catch (Exception $e) {
                if ($this->causedByLostConnection($e)) {
                    $this->reconnect();
                    $this->pdo->beginTransaction();
                } else {
                    throw $e;
                }
            }
        } elseif ($this->transactions >= 1 && $this->queryGrammar->supportsSavepoints()) {
            $this->getPdo()->exec(
                $this->queryGrammar->compileSavepoint('trans'.($this->transactions + 1))
            );
        }

        ++$this->transactions;

        $this->fireConnectionEvent('beganTransaction');
    }
```
> ↑ 开启事务时检测当前transactions等级，如果等于1开启事务，如果大于1则创建相应level的savepoint。
> 在第一次使用 `beginTransaction` 时，$this->transactions 为默认值 0，当执行完 pdo 的 beginTransaction 后，
> 这时就执行了 `++$this->transactions` , 此时 $this->transactions 变为 1，
> 当第 2 个 beginTransaction 方法执行时
```php
    /**
     * Commit the active database transaction.
     *
     * @return void
     */
    public function commit()
    {
        if ($this->transactions == 1) {
            $this->getPdo()->commit();
        }

        $this->transactions = max(0, $this->transactions - 1);

        $this->fireConnectionEvent('committed');
    }
``` 
- ↑ commit操作时候，检测当前transactions等级，如果不等于1跳过操作，并且transactions等级减1。如果等于1，事务提交。

```php
    /**
     * Rollback the active database transaction.
     *
     * @return void
     */
    public function rollBack()
    {
        if ($this->transactions == 1) {
            $this->getPdo()->rollBack();
        } elseif ($this->transactions > 1 && $this->queryGrammar->supportsSavepoints()) {
            $this->getPdo()->exec(
                $this->queryGrammar->compileSavepointRollBack('trans'.$this->transactions)
            );
        }

        $this->transactions = max(0, $this->transactions - 1);

        $this->fireConnectionEvent('rollingBack');
    }
```
 
- ↑ 而rollback操作，检测当前transactions等级，如果不等于1回滚到相应等级的savepoint，等于1这全部回滚。

### 其他相关资料：
- http://www.jb51.net/article/60921.htm [PHP中实现MySQL嵌套事务的两种解决方案]

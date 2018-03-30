案例１：老算法：打印输出当前时间　凌晨＼上午＼下午＼晚上
```php
function A()
{
    $hour = date('G');

    if ($hour < 6) {
        $str = '凌晨';
    } elseif ($hour < 12) {
        $str = '上午';
    } elseif ($hour < 18) {
        $str = '下午';
    } else {
        $str = '晚上';
    }

    return $str;
}
```
案例１：新算法
```php
function A(): string
{
    return ['凌晨', '上午', '下午', '晚上'][floor(date('G') / 6)];
}
```
案例２：老算法：根据时间打印输出是星期几
```php
function A($date)
{
    $weekday = array('星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六');
    $date = str_replace('/', '-', $date);
    $dateArr = explode('-', $date);
    return $weekday[date('w', mktime(0, 0, 0, $dateArr[1], $dateArr[2], $dateArr[0]))];
}
```
案例２：新算法
```php
function A(string $date): string
{
    return '星期'.['日', '一', '二', '三', '四', '五', '六'][date('w', strtotime($date))];
}
```
案例３：老算法：PHP二维数组转一维数组，键下标的使用
```php
function A($eid = '')
{
    $managerList = ＤＢ获得的二维数组值;

    $user_id = $admin_uid = '';
    if (!empty($managerList)) {

        foreach ($managerList as $user) {
            if ($user->user_id == 'admin') {
                $admin_uid = 'admin';
                break;
            }

            if (!empty($user->user_id)) {
                $user_id = $user->user_id;
                break;
            } else {
                $user_id = 'admin';
            }
        }

        $user_id = $admin_uid ? $admin_uid : $user_id;
    }

    return $user_id;
}
```
案例３：新算法
```php
function A($eid = '')
{
    $managerList = array_column(ＤＢ获得的二维数组值, 'user_id', 'user_id');
    return isset($managerList['admin']) ? 'admin' : (string) current($managerList);
}
```
案例４：老算法：三元表达式在强类型下的快速转换
```php
if ($data) {
    return true;
}

return false;
```
案例４：新算法
```php
return (bool) $data;
```

案例５：老算法：根据时间返回具体周的具体时期，时间计算表达式
```php
function A($year, $week = 1)
{
    $year_start = mktime(0, 0, 0, 1, 1, $year);
    $year_end = mktime(0, 0, 0, 12, 31, $year);
    
    // 判断第一天是否为第一周的开始
    if (intval(date('W', $year_start)) == 0) {
        $start = $year_start; // 把第一天做为第一周的开始
    } else {
        $start = strtotime('+1 sunday', $year_start); // 把第一个周日作为开始
    }
    
    // 第几周的开始时间
    if ($week === 1) {
        $weekday['start'] = $start;
    } else {
        $weekday['start'] = strtotime('+' . $week . ' sunday', $start);
        $week ++;
    }
    return date('Y-m-d H:i:s', $weekday['start']);
}
```
案例５：新算法
```php
function A(int $year = 2009, string $week = '01'): string
{
    return date('Y-m-d H:i:s', strtotime($year.'W'.$week.' -1 day'));
    //return date('Y-m-d 23:59:59', strtotime($year.'W'.$week.' +5 day'));
}
```
案例６：老算法：MySQL新特性，有则更新　无则插入　事务代替循环
```php
public static function A($entIds, $path = false, $del = false)
{
    if ($path === true) {
        $entList = \LibUser::getEnts(\Common::getUserId());
        if (empty($entList)) {
            foreach ($entIds as $entId) {
                $result = \Dbio::queryScalar(
                    [
                        'SELECT 1 FROM `A` WHERE `id` = ?',
                        [$entId]
                    ]
                );
                if ($result) {
                    \Dbio::execute(
                        [
                            "UPDATE `A` SET `record` = `record` + 1 WHERE `id` = ?",
                            [$entId]
                        ]
                    );
                } else {
                    \Dbio::execute(
                        [
                            'INSERT INTO `A` (`id`, `record`) VALUES (?, ?);',
                            [$entId, 1]
                        ]
                    );
                }
            }
        } else {
            foreach ($entList as $entId) {
                $result = \Dbio::queryScalar(
                    [
                        'SELECT 1 FROM `A` WHERE `id` = ?',
                        [$entId['id']]
                    ]
                );
                if ($result) {
                    \Dbio::execute(
                        [
                            "UPDATE `A` SET `record` = `record` + 1 WHERE `id` = ?",
                            [$entId['id']]
                        ]
                    );
                } else {
                    \Dbio::execute(
                        [
                            'INSERT INTO `A` (`id`, `record`) VALUES (?, ?);',
                            [$entId['id'], 1]
                        ]
                    );
                }
            }
        }
    } else {
        if ($del === true) {
            \Dbio::execute(
                [
                    'DELETE FROM `A` WHERE `id` = ?',
                    [$entIds]
                ]
            );
        } else {
            $result = \Dbio::queryScalar(
                [
                    'SELECT 1 FROM `A` WHERE `id` = ?',
                    [$entIds]
                ]
            );
            if ($result) {
                \Dbio::execute(
                    [
                        "UPDATE `A` SET `record` = `record` + 1 WHERE `id` = ?",
                        [$entIds]
                    ]
                );
            } else {
                \Dbio::execute(
                    [
                        'INSERT INTO `A` (`id`, `record`) VALUES (?, ?);',
                        [$entIds, 1]
                    ]
                );
            }
        }
        
    }
    
}
```
案例６：新算法
```php
function userChangeRecord(array $entIds, bool $path = false, bool $del = false): bool
{
    $insertSql = 'INSERT INTO `A`(`id`, `record`) VALUES(?,?) ON DUPLICATE KEY UPDATE `record`=`record`+1;';
    if ($path) {
        $sqlArray = [];
        $entList = $entIds ? $entIds : array_column(\LibUser::getEnts(\Common::getUserId()), 'id');
        foreach ($entList as $entId) {
            $sqlArray[] = [$insertSql, [$entId, 1]];
        }
        return \Dbio::transaction($sqlArray);
    } else {
        return $del ? \Dbio::execute([$insertSql, [$entIds, 1]]) : \Dbio::execute(['DELETE FROM `A` WHERE `id` = ?', [$entIds]]);
    }
}
```

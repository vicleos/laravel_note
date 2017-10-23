
#### 二进制求法:
```php

<?php
//1.0 用数组模拟一个非空集合
$arr = array(1,2,3);
$arr = array_unique($arr);

//2.0 求出这个集合的子集,并将子集存放至数组
$n = count($arr);
$sub_n = pow(2,$n);
$sub_array = array();

for($i=0; $i<$sub_n; $i++){
    $m = sprintf('%0+'.$n.'b',$i);
    $t_arr = array();
    for($j=0;$j<$n;$j++)
        if($m{$j}==1 && $j!=$n) $t_arr[] = $arr[$j];
    $sub_array[] = '{'.implode(',', $t_arr).'}';
}
//3.0输出
var_dump($sub_array);

```
- 结果：
```php
array:8 [▼
  0 => "{}"
  1 => "{3}"
  2 => "{2}"
  3 => "{2,3}"
  4 => "{1}"
  5 => "{1,3}"
  6 => "{1,2}"
  7 => "{1,2,3}"
]
```
#### 直接遍历(递归):
```php
<?php
function set($part='',$s=0)
{
    $arr= array(1,2,3);
    echo '{'.trim($part,',').'}<br>';
    for($start=$s;$start<count($arr);$start++)
    {
       set($part.','.$arr[$start],$start+1);
    }
}
set();
```
- 结果：
```php
{}
{1}
{1,2}
{1,2,3}
{1,3}
{2}
{2,3}
{3}
```

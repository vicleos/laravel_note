#### 二分查找采用的方法比较容易理解，以数组为例，

- 先取数组中间的值floor((low+top)/2),
- 然后通过与所需查找的数字进行比较，若比中间值大，则将首值替换为中间位置下一个位置，继续第一步的操作；若比中间值小，则将尾值替换为中间位置上一个位置，继续第一步操作
- 重复第二步操作直至找出目标数字 
- 比如从1，3，9，23，54 中查找数字23， 
- 首位置为0， 尾位置为4，中间位置就为2 值为9，比23小，则首位置更新为2+1即3；那么接下来中间位置就为（3+4）/2=3，值为23，比较相等即找到
```php
// 非递归
// $target是要查找的目标 $arr是已经排序好的数组
function binary(&$arr, $low, $top, $target){
    while($low <= $top){
        //由于php取商是有小数的，所以向下取整，不过也可不加，数组也会取整
        $mid = floor(($low + $top)/2);
        if($arr[$mid] == $target){
            return $mid;
        }
        if($arr[$mid] < $target){
            $low = $mid + 1;                
        }else{
            $top = $mid - 1;
        }
    }
    return false;
}
$arr = array(1,3,9,23,54);
echo binary($arr, 0, sizeof($arr), 9);
//2
```
```php
// 递归
function binaryRecursive(&$arr, $low, $top, $target){
    if($top > $low){
        return false;
    }
    $mid = floor(($low + $top)/2);
    if($arr[$mid] == $target){
        return $mid;
    }
    if($arr[$mid] < $target){
        return binaryRecursive($arr, $mid + 1, $top, $target);
    }
    return binaryRecursive($arr, $low, $mid - 1, $target);
}
$arr = array(1,3,9,23,54);
echo binaryRecursive($arr, 0, sizeof($arr), 9);
//2
```

#### 使用 $query->select('xxxx') 后 withCount 会无效
- 正确的使用方法为：
```php
$query = $this->model->withCount(['hasManyErShouFang as esf_real_count' => function($query){
      // dd($query->toSql())
}]);
$query = $query->addSelect(\DB::raw('xxxxx')) ......

```
- 大概 SQL 语句
```
select `tb1`.*, (select count(*) from `tb2` where `tb1`.`tb1_id` = `tb2`.`tb2_id`) as `xxx_count`, xxx AS cpt from `tb1` where ...
```

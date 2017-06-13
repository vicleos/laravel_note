  
  #### 如何格式化从数据库中获取的时间戳字段
  
  ```php
  class XXX extends Model
  {
    ...
    //预约时间格式化
    public function getReserveTimeAttribute($date)
    {
        return date('Y-m-d H:i:s', $date);
    }
    ...
  }
  ```
  
  此时，再通过 ORM 获取的数据集则会自动将 `reserve_time` 字段的时间戳格式化为 `Y-m-d H:i:s`

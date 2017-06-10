
#### Eloquent model 操作方法文件：
\vendor\laravel\framework\src\Illuminate\Database\Eloquent\Builder.php
在此文件中包含model的大部分方法 如：find

```php
    public function find($id, $columns = ['*'])
    {
        if (is_array($id)) {
            return $this->findMany($id, $columns);
        }

        $this->query->where($this->model->getQualifiedKeyName(), '=', $id);

        return $this->first($columns);
    }
```

#### 开启全局 SQL 执行语句日志
// 所有查询输出到日志文件中
将下面语句复制到 `app\Providers\AppServiceProvider.php` 中的 `boot()` 方法中
```php
\DB::listen(function($query) { \Log::info(json_encode($query)); });
```

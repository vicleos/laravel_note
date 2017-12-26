- 文件位置：app/Providers/AppServiceProvider.php
```php
class AppServiceProvider extends ServiceProvider
...
public function boot(){
  ...
  if (!isProduction()) {
    // 所有查询输出到日志文件中 vicleo 20170518
    //\DB::listen(function($query) { \Log::info(json_encode($query, JSON_UNESCAPED_UNICODE)); });
  }
  ...
}
...
```

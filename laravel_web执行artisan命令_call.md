### laravel web 执行 Artisan 命令并返回输出结果 
- 实例：
```php
public function doArtisan(Request $rq){
  ···
  $exitCode = Artisan::call('api:routes');
  dd(Artisan::output());
  ···
}
```

- 备注：
Artisan::call() 方法来自于文件 vendor\laravel\framework\src\Illuminate\Console\Command.php

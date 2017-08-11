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
- Artisan::call() 和 Artisan::output() 方法均来自于文件 vendor\laravel\framework\src\Illuminate\Console\Application.php

- Artisan::output() 获取最后一次执行命令的输出信息

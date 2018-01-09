##### http://www.cnblogs.com/chunguang/p/5660074.html

Artisan是Laravel自带的命令行接口名称,它提供了很多有用的命令想要查看所有可用的Artisan命令,可使用list命令查看:
```
php artisan list
```
每个命令都可以用help指令显示命令描述及命令参数和选项。想要查看帮助界面，只需要在命令前加上help就可以了,例如：
```
php artisan help migrate
```
除了Artisan提供的命令之外，还可以构建自己的命令。可以将自定义命令存放在app/Console/Commands目录；当然，也可以自己选择存放位置，只要改命令可以基于composer.json被自动加载。

要创建一个新命令，可以使用Artisan命令make:console,比如我要创一个发送邮件的artisan命令,可以这样：

```
php artisan make:console SendEmails
```
上述命令将会生成一个类app/Console/Commands/SendEmails.php,当创建命令时，--command选项可用于分配终端命令名（在终端调用命令时用）：

```
php artisan make:console SendEmails --command=emails:send
```
命令生成以后，需要填写该类的signature和description属性，这两个属性在调用list显示命令的时候会被用到。handle方法在命令执行时被调用，可以将所有命令逻辑都放在这个方法里面,我们可以在命令控制器的构造函数中注入任何依赖.这个SendEmails.php里面内容参考如下:
```
<?php namespace App\Console\Commands;
 
use Illuminate\Console\Command;
 
class SendEmails extends Command {
 
    /**
     * The console command name.
     *
     * @var string
     */
    protected $name = 'emails:send';
 
    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = '这是发邮件的命令.';
 
    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }
 
    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        //TODO:发送邮件逻辑
    }
 
}
```
$name是这个命令的名称,即artisan调用时的命令,如本例命令设为了emails:send,那么实际调用时要这么用:

```
php artisan emails:send
```
执行上面这条命令就是执行handle()方法,当然,这里还漏了一个非常重要的关键步骤,那就是需要把命令注入到app/Console/Kernel.php文件中,否则这个命令artisan是找不到的,示例如下:

```
<?php namespace App\Console;
 
use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
 
class Kernel extends ConsoleKernel {
 
    /**
     * The Artisan commands provided by your application.
     *
     * @var array
     */
    protected $commands = [
        'App\Console\Commands\Inspire',
        'App\Console\Commands\SendEmails',
    ];
 
    /**
     * Define the application's command schedule.
     *
     * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
     * @return void
     */
    protected function schedule(Schedule $schedule)
    {
        $schedule->command('inspire')
                 ->hourly();
    }
 
}
```
关键就是在$commands里面把要用到的SendEmails类放进去,好了,这样就可以通过artisan命令来执行脚本了.

由于artisan命令需要在Laravel的目录里面才能执行,所以实际要用crontab调用artisan命令时需要注意Crontab的shell代码要这样写,切记非常重要,否则是执行了不会运行实际处理逻辑的.

```
30 1 * * *    php /www/projects/laravelapp/artisan emails:send
```
上面/www/projects/laravelapp/是项目的路径


定时任务：

Laravel有内置命令调度器,可以方便的实现Cron.

任务调度定义在app/Console/Kernel.php文件的schedule方法中,该方法已经包含了一个示例.Laravel里有两种方法执行Cron,第一种方法是让Cron每分钟调用Laravel命令调度,然后让Laravel来根据具体的命令来实现;需要在crontab里面加入如下内容:
```
* * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1
```

然后在上面的Kernel.php的schedule中添加任务

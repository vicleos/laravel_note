- from : http://blog.51cto.com/wangzhiqiang/1856846
> 单点登录 SSO ( Single Sign On ) 这个术语大家都听说过, 为什么要单点登录? 比如: 视频教程网站, 如果一个帐号买了1个课程, 然后在把自己的帐号共享给其他人, 那其他人也能在他看视频的同时也登录他的账号看视频了, 那公司的利益就受到了损失, 那帐号如果分给 1000 人, 10000 人, 这损失就不小,如果做了SSO 就起码可以保证每个账号只能同时一个人登录 那么今天带着大家做一下单点登录的实例。

##### 涉及技术
- Laravel
- 路由
- 中间件
- Redis

这里我使用的 Laravel 5.1 LTS 框架, 登录逻辑, 挺简单的这里就简单的阐述下, 我们只要在登录成功之后做一点 手脚

##### 登录
```php
// 登录验证
$result = \DB::table('user_login')->where(['username' => $input['username'], 'password' => $input['pass']])->find();
...
...
// 该地方为登录验证逻辑
if ($result) {
    # 登录成功
    // 制作 token
    $time = time();
    // md5 加密
    $singleToken = md5($request->getClientIp() . $result->guid . $time);
    // 当前 time 存入 Redis
    \Redis::set(STRING_SINGLETOKEN_ . $result->guid, $time);
    // 用户信息存入 Session
    \Session::put('user_login', $result);
    // 跳转到首页, 并附带 Cookie
    return response()->view('index')->withCookie('SINGLETOKEN', $singletoken);
} else {
    # 登录失败逻辑处理
}
```
> 我来解释一下: 首先登录成功之后, 得到目前时间戳, 通过 IP, time, 和 查询得出用户的 Guid 进行MD5 加密, 得到 TOKEN 然后我们将刚刚得到的时间戳, 存入 Redis Redis Key 为字符串拼接上Guid, 方便后面中间件的 TOKEN 验证, 然后我们把用户信息存入 Session 最后我们把计算的TOKEN 以 Cookie 发送给客户端.

##### 中间件

我们再来制作一个中间件, 让我们用户每一次操作都在我们掌控之中.

```php
// 项目根目录运行
php artisan make:middleware SsoMiddleware
```
上面个命令会在 app/Http/Middleware 下面生成一个 SsoMiddleware.php 文件, 将中间件添加到Kernel.php
```php
/**
 * The application's route middleware.
 *
 * @var array
 */
protected $routeMiddleware = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
    'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    'SsoMiddleware' => \App\Http\Middleware\index\SsoMiddleware::class,
];
```
现在到中间件中写程序 app/Http/Middleware/SsoMiddleware.php, 在文件中有 handle 方法, 我们在这个方法中写逻辑.
```php
/**
 * Handle an incoming request.
 *
 * @param  \Illuminate\Http\Request $request
 * @param  \Closure $next
 * @return mixed
 */
public function handle($request, Closure $next)
{
    $userInfo = \Session::get('user_login');
    if ($userInfo) {
        // 获取 Cookie 中的 token
        $singletoken = $request->cookie('SINGLETOKEN');
        if ($singletoken) {
            // 从 Redis 获取 time
            $redisTime = \Redis::get(STRING_SINGLETOKEN_ . $userInfo->guid);
            // 重新获取加密参数加密
            $ip = $request->getClientIp();
            $secret = md5($ip . $userInfo->guid . $redisTime);
            if ($singletoken != $secret) {
                // 记录此次异常登录记录
                \DB::table('data_login_exception')->insert(['guid' => $userInfo->guid, 'ip' => $ip, 'addtime' => time()]);
                // 清除 session 数据
                \Session::forget('indexlogin');
                return view('/403')->with(['Msg' => '您的帐号在另一个地点登录..']);
            }
            return $next($request);
        } else {
            return redirect('/login');
        }
    } else {
        return redirect('/login');
    }
}
```

上面中间件之中做的事情是: 获取用户存在 Session 之中的数据作为第一重判断, 如果通过判断, 进入第二重判断, 先获取我们登录之后发送给用户的 Cookie 在 Cookie 之中会有我们登录成功后传到客户端的 SINGLETOKEN 我们要做的事情就是重新获取存入 Redis 的时间戳, 取出来安顺序和 IP, Guid, time MD5 加密, 加密后和客户端得到的 Cookie 之中的 SINGLETOKEN 对比.

##### 路由组
我们逻辑写完了, 最后一步就是将用户登录后的每一步操作都掌控在自己手里, 这里我们就需要路由组
```php
// 有 Sso 中间件的路由组
Route::group(['middleware' => 'SsoMiddleware'], function() {
    # 用户登录成功后的路由
}
```



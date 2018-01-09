#### https://www.awaimai.com/2203.html
#### http://git.mydoc.io/?t=153693

假设，我们有三个环境：

线上仓库。如Github、GitLab或Gitee（开源中国）
本地仓库。日常开发用的。
服务器仓库。一般是自动在测试服务器，或者生产服务器。
这里我们要达到的目的是，

当有新的本地 commit push 到线上仓库时，服务器仓库自动pull最线上仓库新的代码。

1 工作原理
Webhooks工作原理很简单，如下图。



当我们push 代码到线上仓库，线上仓库必然知道这个push操作，就会hook（回调）我们预留的URL。

而这个URL对应一段后台代码，这段代码执行了git pull，这样就实现下拉代码操作。

上图是以PHP为例，实际上用Java、Javascrtip等都可以，理论上一行代码就可以搞定。

不过实际稍微复杂一点，需要进行一些安全验证。

2 准备工作
首先，我们需要在服务器（生产或者测试等等）做一些准备工作。

最先应该做的，就是在服务器上安装git（哈哈，这个应该都没问题）

然后，克隆代码：

$ cd /var/www/html           # 代码存放目录
$ git clone https://github.com/yeszao/fastphp.git
因为这是公共残酷，所以这里我们使用的是https方式。

如果用SSH方式，需要配置SSH KEY，请参考这里。

克隆完成后，代码就在这个目录里面了：

/var/www/html/fastphp
这个就是服务器上的一个网站根目录了，而且通过域名也是可以访问其下的index.php等文件的。

3 PHP代码
Github、GitLab和Gitee（开源中国，码云）虽然都是git仓库平台，但是发送的webhooks请求的数据格式有些差别。

Github支持application/json和application/x-www-form-urlencoded两种格式，安全token需通过请求头X-Hub-Signature加密发给URL，服务器需要解密后验证。了解更多。
GitLab支持application/json格式，安全token通过请求头HTTP_X_GITLAB_TOKEN明文发给URL。了解更多。
Gitee也支持application/json和application/x-www-form-urlencoded两种格式，安全token放在请求体明文发给URL，名称是password。了解更多。
请求头我们可以通过$_SERVER全局变量获得请求的值，比如$_SERVER['X-Hub-Signature']。

请求体则分为两种：

如果是application/json格式，用这个方式获得：

$payload = json_decode(file_get_contents('php://input'), true);
如果是application/x-www-form-urlencoded，就要用$_POST获得：

$payload = $_POST['payload'];
完整代码如下（GitLab）：

<?php

/ 本地仓库路径
$local = '/var/www/html/awaimai';

// 安全验证字符串，为空则不验证
$token = '123456';


// 如果启用验证，并且验证失败，返回错误
$httpToken = isset($_SERVER['HTTP_X_GITLAB_TOKEN']) ? $_SERVER['HTTP_X_GITLAB_TOKEN'] : '';
if ($token && $httpToken != $token) {
    header('HTTP/1.1 403 Permission Denied');
    die('Permission denied.');
}

// 如果仓库目录不存在，返回错误
if (!is_dir($local)) {
    header('HTTP/1.1 500 Internal Server Error');
    die('Local directory is missing');
}

//如果请求体内容为空，返回错误
$payload = file_get_contents('php://input');
if (!$payload) {
    header('HTTP/1.1 400 Bad Request');
    die('HTTP HEADER or POST is missing.');
}

/*
 * 这里有几点需要注意：
 *
 * 1.确保PHP正常执行系统命令。写一个PHP文件，内容：
 * `<?php shell_exec('ls -la')`
 * 在通过浏览器访问这个文件，能够输出目录结构说明PHP可以运行系统命令。
 *
 * 2、PHP一般使用www-data或者nginx用户运行，PHP通过脚本执行系统命令也是用这个用户，
 * 所以必须确保在该用户家目录（一般是/home/www-data或/home/nginx）下有.ssh目录和
 * 一些授权文件，以及git配置文件，如下：
 * ```
 * + .ssh
 *   - authorized_keys
 *   - config
 *   - id_rsa
 *   - id_rsa.pub
 *   - known_hosts
 * - .gitconfig
 * ```
 *
 * 3.在执行的命令后面加上2>&1可以输出详细信息，确定错误位置
 *
 * 4.git目录权限问题。比如：
 * `fatal: Unable to create '/data/www/html/awaimai/.git/index.lock': Permission denied`
 * 那就是PHP用户没有写权限，需要给目录授予权限:
 * ``
 * sudo chown -R :www-data /data/www/html/awaimai`
 * sudo chmod -R g+w /data/www/html/awaimai
 * ```
 *
 * 5.SSH认证问题。如果是通过SSH认证，有可能提示错误：
 * `Could not create directory '/.ssh'.`
 * 或者
 * `Host key verification failed.`
 *
 */
echo shell_exec("cd {$local} && git pull 2>&1");
die("done " . date('Y-m-d H:i:s', time()));
GitHub验证方式请看：https://gist.github.com/milo/daed6e958ea534e4eba3

4 Webhooks配置
4.1 Github


4.2 Githab


4.3 Gitee
请求数据格式默认是application/json格式，application/x-www-form-urlencoded格式的话需要选择：Old format。



5 测试
以上我们都订阅了push事件。

这样只要我们本地仓库有push命令，都会执行一遍服务器仓库的git pull操作。

git push -u origin master

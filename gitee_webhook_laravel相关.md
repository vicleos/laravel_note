```php
/**
     * git 仓库相关 web hook
     * www 用户的公钥 在 /home/www/.ssh/id_rsa.pub 中
     * @param Request $request
     */
	public function gitWebHook(Request $request)
    {
        Log::info('git web hook callback : '.json_encode($request->all(), JSON_UNESCAPED_UNICODE));
        // TODO 当回滚时，要避免直接执行git pull，需要人为控制
        // 仓库路径
        $local = '/www/wwwroot/zgengine';

        // 安全验证字符串，为空则不验证 Gitee 密码串, 暂不验证
        $token = '';

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
         * 参考：https://www.jianshu.com/p/4eac43872b40
         * 1.确保PHP正常执行系统命令。写一个PHP文件，内容：
         * `<?php shell_exec('ls -la')`
         * 在通过浏览器访问这个文件，能够输出目录结构说明PHP可以运行系统命令。
         *
         * 2、PHP一般使用www用户运行，PHP通过脚本执行系统命令也是用这个用户，
         * 所以必须确保在该用户家目录（一般是/home/www）下有.ssh目录和
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
         * 2.1 、如果www用户目录不存在.ssh，那么要进入 /home/www/.ssh 目录中
         * ```
         * 执行：ssh-keygen
         * ```
         * - 执行完毕后，复制 id_rsa.pub 内容，添加到部署公钥
         * 3.在执行的命令后面加上2>&1可以输出详细信息，确定错误位置
         *
         * 4.git目录权限问题。比如：
         * `fatal: Unable to create '/data/www/html/awaimai/.git/index.lock': Permission denied`
         * 那就是PHP用户没有写权限，需要给目录授予权限:
         * ``
         * sudo chown -R :www /www/wwwroot/zgengine`
         * sudo chmod -R g+w /www/wwwroot/zgengine
         * ```
         */
        echo shell_exec("cd {$local} && git pull 2>&1");
        die("done " . date('Y-m-d H:i:s', time()));
    }
  ```

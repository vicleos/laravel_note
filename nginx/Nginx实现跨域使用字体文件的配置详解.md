
##### 问题：
- 子域名访问根域名的CSS时，发现字体无法显示，在确保CSS和Font字体的路径加载无问题后，基本确定是因为跨域的问题。

#### 解决方案:
- 通过Nginx模块Http_Headers_Module来添加Access-Control-Allow-Origin允许的地址

- 修改 `vhost` 中的 `xxx.conf`文件内容，添加下面的内容：
- `指定域名： add_header Access-Control-Allow-Origin http://xxx.xxx.com;`
```bash
location ~* \.(eot|ttf|woff|svg|otf)$ {
  add_header Access-Control-Allow-Origin *;
  add_header Access-Control-Allow-Headers X-Requested-With;
  add_header Access-Control-Allow-Methods GET,POST,OPTIONS;
}
```
- 设置完重启 `nginx` 服务器
```
service nginx restart
```
- 刷新页面重新访问


#### Qiniu: -1 Could not resolve host http. 错误：
原因是不能在 `UPLOAD_DOMAIN_DEFAULT` 域名前加 `http://` 之类的协议，
把配置文件中的 `UPLOAD_DOMAIN_DEFAULT` 值中的 `http://` 去掉即可。
如：
```
UPLOAD_DOMAIN_DEFAULT=xxxx.bkt.clouddn.com
```

#### 安装vagrant 插件 vagrant-winnfsd
- 方式1：(可能会比较慢)
```bash
$ vagrant plugin install vagrant-winnfsd
```
- 方式2：下载到本地安装
- 下载地址：
- https://rubygems.org/gems/childprocess-0.5.8.gem
- https://rubygems.org/gems/vagrant-winnfsd-1.1.0.gem
```bash

vagrant plugin install childprocess-0.5.8.gem
vagrant plugin install vagrant-winnfsd-1.1.0.gem

```
- 查看已安装的插件列表
```bash
$ vagrant plugin list
childprocess (0.5.8)
  - Version Constraint: 0.5.8
vagrant-share (1.1.4, system)
vagrant-winnfsd (1.1.0)
  - Version Constraint: 1.1.0
```
- 编辑项目下的 Vagrantfile 文件
```
Vagrant.configure('xxxxxxxx') do |config|
  #winfsd
  #config.winnfsd.logging = "on" #开了这个会很卡的哟
  config.winnfsd.uid = 1
  config.winnfsd.gid = 1
end
```

- vagrant 重启或重新加载配置
```bash
vagrant provision
vagrant reload
```

在启动过程中，看到下面的这几条就代表成功了
```bash
···
==> default: Exporting NFS shared folders...
==> default: Preparing to edit nfs mounting file.
[NFS] Status: halted
[NFS] Start: started
==> default: Mounting NFS shared folders...
==> default: Mounting shared folders...
    default: /vagrant => E:/wwwroot
···
```

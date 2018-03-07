- 先安装nodejs ，怎么安装Nodejs就不在这里阐述了

##### Windows 7
```bash
# 克隆示例项目的仓库
D:\client\electron-quick-start> git clone https://github.com/electron/electron-quick-start

# 进入这个仓库
D:\client\electron-quick-start> cd electron-quick-start

# 安装依赖并运行
D:\client\electron-quick-start> npm install
D:\client\electron-quick-start> npm start
```
- 打包为exe
```bash
# 全局安装 electron-packager
D:\client\electron-quick-start> npm -g install electron-packager
D:\client\electron-quick-start> electron-packager . --platfrom-win32 --arch-x64
```
- 完毕
```
# 打包好的 exe 文件就在 electron-quick-start-win32-x64 文件夹中
# 运行 electron-quick-start.exe 即可
```

- 备注：
> 只有在 npm start 的时候，才会出现顶部的菜单栏，如File, Edit, View, Window 之类的

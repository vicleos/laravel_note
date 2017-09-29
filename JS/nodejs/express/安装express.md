
- homestead 3 中：
```bash
sudo npm install -g express
express -e nodejs-demo
cd nodejs-demo
sudo npm install
```
- 如果不存在 `express` 命令，则需要安装相关依赖
```bash
sudo npm install -g express-generator
```
- 启动express
```bash
node app.js
```
- 测试是否正常
```bash
curl localhost:3000
```
- 如果显示连接拒绝或者端口被占用，那么需要修改端口
- 在app.js文件中 var app = express(); 下面加入：
```javascript
...
app.listen(3066);
...
```
- 再次 `node app.js`

- 通过node启动程序，每次代码修改都需要重新启动。 有一个工具supervisor，每次修改代码后会自动重启，会我们开发省很多的时间。
```bash
sudo npm install -g supervisor
```
- 再次启动
```bash
supervisor app.js
```

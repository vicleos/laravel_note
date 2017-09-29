
- homestead 3 中：
```bash
sudo npm install -g express
express -e nodejs-demo
cd nodejs-demo
sudo npm install
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

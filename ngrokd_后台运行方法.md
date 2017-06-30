
- ngrok 用 & 不能后台运行 
- 这就要使用screen这个命令
- 首先安装screen
```bash
apt-get install screen
```
- 进入到 `ngrokd` 所在的 `bin` 目录 ( 例如：`/usr/local/ngrok/bin` )
- 之后运行 `screen -S` 任意名字（ 例如：`techapi` ）
- 然后运行ngrok启动命令 ( 例如：`./ngrokd -domain="test.xxx.com" -httpAddr=":9999" -httpsAddr=":8089"` )
- 最后按快捷键 `ctrl+A+D` 既可以保持ngrok后台运行

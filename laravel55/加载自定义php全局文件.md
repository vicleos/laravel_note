- 比如我们要全局调用 Yyy.php，那么我们就在composer.json 的 autoload 中的 files 中添加我们的文件
```json
"autoload": {
    "classmap": [
        "database/seeds",
        "database/factories"
    ],
    "files": [
        "app/Xxx/Yyy.php"
    ],
    "psr-4": {
        "App\\": "app/"
    }
},
```
- 添加完以后，要执行 composer auto-dumpload 来重新生成 autoload 文件

#### mac 下安装 `gulp`：
- brew install nodejs
- npm init
- npm install gulp
#### 创建好 `gulpfile.js` 文件：
- 示例：
```js
var gulp = require('gulp');

gulp.task('default', function(){
    console.log('hello gulp!');
});
```

#### 执行 `gulp`
```bash
./node_modules/.bin/gulp
```
- 输出结果：
```bash
[23:48:53] Using gulpfile ~/code/xxx/gulpfile.js
[23:48:53] Starting 'default'...
hello gulp!
[23:48:53] Finished 'default' after 138 μs
```

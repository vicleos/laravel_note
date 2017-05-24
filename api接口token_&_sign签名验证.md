### 小程序 & PHP 实现与 APP 后端接口通过 token 和 sign 交互
---
#### 客户端请求方式及签名参数组成方式

以小程序中的 JS 请求作为例子：

- `md5.js`代码 [https://github.com/vicleos/laravel_note/blob/master/wxxcx/js/md5.js]

```javascript
...
var md5 = require('/utils/md5.js'); 
...
let params = {
  'sign': md5.hexMD5(wx.getStorageSync('_api_token') + timestamp + 'JKG').toUpperCase(),
  'api_token' : wx.getStorageSync('_api_token'),
  'timestamp': timestamp
};
post('/auth', params).then(data => {
  if(data.status == false){
    wx.setStorageSync('_api_token', '');
    wx.setStorageSync('user_info', '');
    wx.navigateTo({
      url: '/pages/login/login'
    });
    return false;
  }
});
```

### 小程序 & PHP 实现与 APP 后端接口通过 token 和 sign 交互
---
#### 客户端请求方式及签名参数组成方式

以小程序中的 JS 请求作为例子：

```javascript
...
var md5 = require('/utils/md5.js'); 
...
let params = {
  'sign': md5.hexMD5(wx.getStorageSync('_token') + timestamp + 'XKey').toUpperCase(),
  'api_token' : wx.getStorageSync('_token'),
  'timestamp': timestamp
};
post('/auth', params).then(data => {
  if(data.status == false){
    wx.setStorageSync('_token', '');
    wx.setStorageSync('_user_info', '');
    wx.navigateTo({
      url: '/pages/login/login'
    });
    return false;
  }
});
```
- `md5.js` 代码 [https://github.com/vicleos/laravel_note/blob/master/wxxcx/js/md5.js]
- `XKey` 是由后端提供的自定义的字符串

### PHP 后端接口验证示例
---
#### 某控制器内
```php
/**
 * 检查签名相关数据是否合法
 * 签名 sign 生成规则 : 客户端 md5(token + timestamp + 'XKey')
 * 单次请求的有效期为 timestamp + 360s
 * @return [type] [description]
 */
public function checkSignData($token = '')
{
    //检查签名时间戳是否在有效期内
    $isTimeOut = $this->timestamp + 360 < time();
    //通过加密后的合成参数与签名对比，检查数据一致性
    $paramsIsValid = strtoupper(md5($token.$this->timestamp.'XKey')) === $this->sign;

    if(!$isTimeOut && $paramsIsValid){
        return true;
    }
    return false;
}
```
写到这，其实也就够了 XD ~ 


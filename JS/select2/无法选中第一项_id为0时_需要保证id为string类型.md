#### 通过 ajax 获取到数据：
```javascript
$(".select_something").select2({
    theme: "bootstrap",
    language:'zh-CN',
    placeholder:'按名称、编号搜索',
    allowClear:true,
    ajax: {
        url: 'xxxxx',
        dataType: 'JSON',
        delay: 250,
        type:'POST',
        data: function (params) {
            return {
                search: params.term
            };
        },
        processResults: function (data) {
            return {
                results: data
            };
        },
        cache: true
    },
    minimumInputLength: 1,
});
```
- 数据获取正常，但是就是无法选中第一个参数
```php
// 我的第一个参数是这样的
$results[] = [
    'id' => 0,  // 这个问题就是这里引起的，必须改为 '0' string类型的值才可以
    'text' => '默认选项'
];
```
- 原因如下：
> The problem is actually that your id is not a string. Because of this, we are doing checks and '' == 0, so it's not changing from the placeholder. When you use a string though, '' != '0', and the first option can be set.

Also, a <select> tag is not self-closing. You should be using <select></select>.

- https://jsfiddle.net/31ph7yk3/5/

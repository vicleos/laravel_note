- 直接上代码：

```javascript
   function strHighLight(str) {
        // 循环所有类名为 .some-str-class 元素，依次替换匹配到的内容
        $.each($('.some-str-class'), function(index, thisItem){
	        var html = $(thisItem).html().replace("#" + str + "#",'<label class="red">#'+ str +'#</label>');
	        $(thisItem).html(html);
    	});
    };
```

- 资料参考：
- http://www.w3school.com.cn/jsref/jsref_replace.asp  【JavaScript replace() 方法】
- http://www.w3school.com.cn/jquery/traversing_each.asp  【jQuery 遍历 - each() 方法】

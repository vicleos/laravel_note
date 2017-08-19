#### php链式调用如果在new实体之后马上调用方法 正确示例：

```php
$someModel->someFunction( ( new MyClass() )->setData('1')  );
```

- 错误示例：
- new MyClass()->setData('1'); 这样使用会报错

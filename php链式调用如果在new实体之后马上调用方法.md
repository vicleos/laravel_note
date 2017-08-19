#### php链式调用如果在new实体之后马上调用方法 示例：

```php
$someModel->someFunction( ( new MyClass() )->setData('1')  );
```

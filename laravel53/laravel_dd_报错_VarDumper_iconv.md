#### laravel dd报错:

- 在laravel5.x使用dd报错

```html
Call to undefined function Symfony\Component\VarDumper\Dumper\iconv_strlen()
```

#### 解决方法： 

- 在项目中运行
```bash
composer require symfony/polyfill-iconv
```

- 安装完成后，再使用dd成功
```php
array:2 [▼
  "xxxx" => "xxx"
]
```

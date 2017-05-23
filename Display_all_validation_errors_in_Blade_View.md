
每个 Blade 视图都有一个 `$errors` 变量(该变量名称可以自定义，这里暂不描述)，在控制器的基础验证中你可以用以下方法输出返回错误
PHP
```php
if ($validator->fails())
{
   return Redirect::to('/profile')
    ->withErrors($validator)
    ->withInput();
}
```
验证的错误信息用上面控制器中的 `withErrors` 方法输出后，我们可以通过下面的方式来显示错误：
```php
@if($errors->has())
   @foreach ($errors->all() as $error)
      <div>{{ $error }}</div>
  @endforeach
@endif
```

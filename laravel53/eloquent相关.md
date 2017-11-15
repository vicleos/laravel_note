#### 使用laravel的Eloquent模型获取数据库的指定列
>
> 使用Laravel的ORM——Eloquent时，时常遇到的一个操作是取模型中的其中一些属性，对应的就是在数据库中取表的特定列。
> - 如果使用DB门面写查询构造器，那只需要链式调用select()方法即可：
> 
```php
$users = DB::table('users')->select('name', 'email as user_email')->get();
```
> 
> 使用Eloquent的话，有两种方式：
> 1. 使用select()
> 
```php
$users = User::select(['name'])->get();
```
> 
> 2. 直接将列名数组作为参数传入all()/get()/find()等方法中
```php
1 $users = User::all(['name']);
2 $admin_users = User::where('role', 'admin')->get(['id', 'name']);
3 $user = User::find($user_id, ['name']);
```
>
> 在关联查询中使用同理：
```php
$posts = User::find($user_id)->posts()->select(['title'])->get();
$posts = User::find($user_id)->posts()->get(['title', 'description']);
```
- 注意这里不能使用动态属性（->posts）来调用关联关系，而需要使用关联关系方法（->posts()）。

我们都知道通过Laravel中数据库查询出来的模型对象都是基于数据库字段，今天给大家展示一个 `Laravel Eloquent ORM` 模型特性-附加值不存在于数据表中。

举个简单的栗子，一篇文章(`posts表`)对应有很多评论(`comments表`)，我们获取文章的同时需要获取评论数量。通常的做法就是根据 ORM 的关联关系，获取评论数量：`$post->comments()->count()` 。

如果获取的是一个文章列表，那么最直接的办法就是 `froeach` 查询出来的文章，然后每篇文章获取评论数量；另外一种做法就是用 `with` 然后在闭包里面实现评论数量，至于怎么实现，我就不详细介绍了。Laravel 提供了一种更优雅的方式。

#### 关联关系#
```php
class Post extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = ['title', 'text'];

    /**
     * 文章对应多条评论
     * @return \Illuminate\Database\Eloquent\Relations\HasMany
     */
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

上面代码没有什么特殊的，只是先声明一下关联关系，接下来会使用。接下来创建一个访问器，如果你还不清楚访问器是什么，建议你看一下Laravel官方文档：https://laravel.com/docs/5.3/eloquent-mutators

#### 创建访问器#

```php
public function getCountCommentsAttribute()
{
    return $this->comments()->count();
}
```
这里的 `getCountCommentsAttribute` 方法名中 get 和 `Attribute` 是固定写法，真正在模型中的名称是由 `CountComments` 决定，命名一般是驼峰写法，一个单词时在 `ORM` 模型中就是那个单词的小写，如果像 `CountComments` 这种方式在 `ORM` 模型会转化为 `count_comments`
创建访问器后，我们获取数据的时候 ORM 模型中并没有这个属性，因为Laravel并不会默认加上访问器的属性。

#### 添加属性到ORM模型中#

我们现在要做的很简单，我们想要在 `ORM` 模型中获取到 `count_comments` 。只用简单的在 `$appends` 数组中添加属性名。
```php
protected $appends = ['count_comments'];
```
OK,That was all！

简单的测试截图：

![Alt text](http://cache.iwanli.me/iwanli/image/QQ%E6%88%AA%E5%9B%BE20161228135846.jpg)


查询出来的ORM中可以看到 `appends` 里面添加了 `count_comments` 属性。把这个 `ORM` 模型进行 `toArray()` 的时候机构就更加清晰了：

### 为什么foreach循环LengthAwarePaginator对象时，只会循环他的item属性？

- 我们在获取一系列分页数据时，通常会得到一个 `LengthAwarePaginator` 对象
- 通过 `dd($xxx)` 后，会看到如下格式:
```php
LengthAwarePaginator {#1318 ▼
  #total: 6
  #lastPage: 1
  #items: Collection {#2064 ▼
    #items: array:6 [▶]
  }
  #perPage: 15
  #currentPage: 1
  #path: "http://xxx.com/xxx"
  #query: []
  #fragment: null
  #pageName: "page"
}
```
- 其中的 `items` 集合就是我们需要的第一页的数据
- 按正常逻辑来说，我们要循环第一页的数据时，肯定是要 `foreach` `items` 中的元素的
- 但是在 `laravel` 中，我们直接 `foreach` 这个 `LengthAwarePaginator` 对象本身就能达到目的

#### 这是为什么呢？如何实现的呢？
- 其实就是 `AbstractPaginator` 类中的 `getIterator` 方法实现的
- `AbstractPaginator` 这个类(抽象类)从哪调用的呢？
- 答案时 `LengthAwarePaginator` 类继承的 `AbstractPaginator`，并且 `implements` 了 `IteratorAggregate` 等众多接口
- 这样 foreach 的时候，foreach 就只会去循环 `getIterator` 方法中的内容了
```php 
// getIterator 方法
/**
     * Get an iterator for the items.
     *
     * @return \ArrayIterator
     */
    public function getIterator()
    {
        return new ArrayIterator($this->items->all());
    }
```

- 到这里应该恍然大悟了哟 XD
#### [参考资料]:
- http://php.net/manual/zh/language.oop5.iterations.php
- http://php.net/manual/zh/iteratoraggregate.getiterator.php
- http://php.net/manual/zh/class.arrayiterator.php


#### 如果在样式类中设置了 position:fixed; 有时会发现点击事件无效

- 原因是页面中的其他层遮盖了该浮动层，所以我们需要在样式中添加 `z-index:9999` 这样的属性
- 最好将事件方式改为非冒泡事件 `catchtap`


#### 关于冒泡事件：
```

事件分类
事件分为冒泡事件和非冒泡事件：

冒泡事件：当一个组件上的事件被触发后，该事件会向父节点传递。
非冒泡事件：当一个组件上的事件被触发后，该事件不会向父节点传递。

----

事件绑定
事件绑定的写法同组件的属性，以 key、value 的形式。

key 以bind或catch开头，然后跟上事件的类型，如bindtap, catchtouchstart
value 是一个字符串，需要在对应的 Page 中定义同名的函数。不然当触发事件的时候会报错。
bind事件绑定不会阻止冒泡事件向上冒泡，catch事件绑定可以阻止冒泡事件向上冒泡。

如在下边这个例子中，点击 inner view 会先后触发handleTap3和handleTap2(因为tap事件会冒泡到 middle view，而 middle view 阻止了 tap 事件冒泡，不再向父节点传递)，点击 middle view 会触发handleTap2，点击 outter view 会触发handleTap1。

```

```html
<view id="outter" bindtap="handleTap1">
  outer view
  <view id="middle" catchtap="handleTap2">
    middle view
    <view id="inner" bindtap="handleTap3">
      inner view
    </view>
  </view>
</view>
```

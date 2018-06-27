```html
<div id="my_test">

<div id="comboMenu">
    <el-tabs type="border-card">
        <el-tab-pane>
            <span slot="label"><i class="el-icon-menu"></i> 已添加菜品</span>
            <el-container>
                <el-main>
                    <div>
                        <div class="mb10">请在套餐中选择商品，即可快速加入套餐中</div>
                        <a class="btn btn-sm btn-info text-white" @click="openComboMenu()">选择菜单商品</a>
                    </div>
                </el-main>
            </el-container>
        </el-tab-pane>
        <el-tab-pane>
            <span slot="label" ref="comboMenu"><i class="el-icon-menu"></i> 菜单</span>
            <el-container>
                <el-header>Header</el-header>
                <el-container>
                    <el-aside width="200px">Aside</el-aside>
                    <el-main>Main</el-main>
                </el-container>
            </el-container>
        </el-tab-pane>
    </el-tabs>
</div>

</div>
```

====

```javascript
let vue = new Vue({
  el: "#my_test",
  data: {},
  methods:{
    openComboMenu:function(){
      console.log(this.$refs);
      this.$refs.comboMenu.offsetParent.click();
    }
  }
}).$mount('#comboMenu');
```
### 主要步骤：
1. 在自定义 `label` 中指定某选项的 `ref` 名称，如：`comboMenu`
2. 在外部按钮添加 `@click="openComboMenu()"` 方法
3. 方法中执行 `this.$refs.comboMenu.offsetParent.click();` 来触发 tab 选项的 `click` 事件

### 参考资料：
- https://cn.vuejs.org/v2/api/#vm-refs
- https://cn.vuejs.org/v2/api/#ref
- https://github.com/ElemeFE/element/blob/076d4303f7b2313f0f9c72be8b53d92ebddfd199/packages/tabs/src/tabs.vue#L122
- 自定义标签页 `slot` 来实现自定义标签页的内容 -> http://element-cn.eleme.io/#/zh-CN/component/tabs#zi-ding-yi-biao-qian-ye

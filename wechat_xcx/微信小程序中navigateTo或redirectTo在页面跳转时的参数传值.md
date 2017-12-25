本文示例微信小程序通过navigateTo或者redirectTo实现连接跳转时的参数传值，可能很多微信小程序开发的新手都清楚pages页面之间的参数传值，类比Web网页开发中的通过url的get的方式实现页面之间的参数的传值，在微信小程序的开发中也是具备这样的功能实现，下面就是示例代码：


参数传值：在inde页面的点击事件中navigate跳转到url，对参数name进行传值hello
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs?name=hello' 
    })
  },

参数接收：在logs的页面中接收来之index页面的参数传值，在logs的js文件中的onLoad的时间事件中进行接受，其中query就是包含name参数的json对象。
Page({
  data: {
    nickname:'default',
    logs: []
  },
  onLoad: function (query) {
    this.setData({
      nickname:query.name
    });
  }
})

wx.navigateTo和wx.redirectTo及中的 query都可以进行页面之间的值的传递。

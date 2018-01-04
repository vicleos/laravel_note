#### 如何设置HTML页面自适应宽度的table(表格)

> WEB应用的页面，表格的表现形式是常常遇到的，在列数有限的前提下，如何将各列中的内容自适应到不同分辨率的屏幕，这应该是一个比较容易遇到的问题，下面就来谈一谈我对这类问题的解决与看法。

将所有列设置为固定宽度，显然是不能满足此类要求的，但是若把全部的列都设置为百分比，恐怕在某些尺寸，或分辨率下，会变得很难看。在Bigtree看来，比较习惯于用如下的方式来处理——在表格列数不是很多的前提下——将大部分列宽用固定值设置死，留下一列不设置宽度，将table的宽度设置为屏幕的百分比（譬如95%、98%等）。
例： <table width="95%" border="1" cellpadding="2" cellspacing="1">   <tr>     <td width="50px" nowrap>序号</td>     <td width="150px" nowrap>分类A</td>     <td width="150px" nowrap>分类B</td>     <td width="200px" nowrap>名称</td>     <td nowrap>说明</td>     <td width="100px" nowrap>操作</td>   </tr>   …… </table>

在本例中，名为“说明”的列，内容比较长，个人认为可以将此列设置为浮动宽度列，用以自适应页面的宽度。

但是当该表格中出现长度比列幅宽的半角字符时，td的宽度会被内容撑破，应该如何解决呢？

解决此问题的方法是：在明细行的td中，追加style="word-wrap:break-word;"，这样做可以使半角连续字符强制换行，不至于撑破列宽。
例：     <td align="left" width="150px" style="word-wrap:break-word;">       ……     </td>

应用此方法，针对设置了width宽度的td列可以解决，但是如果没有设置宽度的td列，是无法生效还是会被撑破td的，应该如何解决呢？

解决此问题的方法是：在定义表格时，追加style="table-layout:fixed;"，这样做可以使半角连续字符强制换行，不至于撑破列宽。需要注意的是，使用此参数后，不要轻易在tr(行)或td(列)中加入height属性，会使table不再被内容撑出适合的高度。
例： <table width="95%" border="1" cellpadding="2" cellspacing="1" style="table-layout:fixed;">   …… </table>

- http://www.cnblogs.com/LBSer/category/475421.html
- https://github.com/taoismCoder/laravel_geohash
- https://tech.meituan.com/lucene-distance.html
- https://www.cnblogs.com/zhenbianshu/p/6863405.html
- http://www.cocoachina.com/programmer/20170821/20309.html
- http://blog.csdn.net/hel12he/article/details/48208927

- http://blog.csdn.net/sunrise_2013/article/details/42024507
- http://www.cnblogs.com/LBSer/p/3310455.html
- https://www.cnblogs.com/hellyliu/p/4870762.html

##### mysql 根据 geohash值 和 多边形节点(GIS) 获取多边形内的坐标
- mysql 5.7 相关手册 
- https://dev.mysql.com/doc/refman/5.7/en/spatial-function-reference.html
- https://dev.mysql.com/doc/refman/5.7/en/spatial-relation-functions-object-shapes.html#function_st-contains
- 表中的 lng, lat 存储着经纬度坐标
- 注意：POLYGON 中的坐标节点要闭合，也就是第一个坐标要和最后一个坐标相同
```sql
select * from (SELECT
	*, ST_GeomFromText (
		'POLYGON((113.455836 34.757087,113.457345 34.759104,113.457848 34.764027,113.443403 34.765865,113.455836 34.757087))') as ste,
	ST_PointFromGeoHash(rst.gh, 0) as rpt
FROM
	( SELECT lng, lat, ST_GeoHash ( lng, lat, 10 ) AS gh FROM spider_house ) AS rst 
WHERE
	rst.gh LIKE 'ww0tt%') as rst_list where st_contains(rst_list.ste, rst_list.rpt) = 1
```

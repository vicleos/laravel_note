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
##### 逻辑思路：
- app获取多边形的(maxLat, minLat, maxLng, maxLng) 和 多边形节点(polygon:[x,x,x,x,x,x]) 发送给接口
- 第一次筛选：根据四个值获取正方形的中心点，计算中心点的geohash值，如：ww0ttxwjby
- 计算需要的参数：中心点geohash值 、 polygon 节点坐标数组(需要闭合，p[0] = p[n])、需要的精度级别、geohash检测精度(like '多少位%')
- 将参数放入上面sql语句中执行，获取最终的筛选结果

##### 另外一种
- app获取多边形的(maxLat, minLat, maxLng, maxLng) 发送给接口
- 第一次筛选：根据四个值获取正方形的中心点，计算中心点的geohash值，如：ww0ttxwjby
- 返回给APP对应的查询结果(like '多少位%')
- app对结果进行筛选，用sdk中的检测点是否在多边形内，去除多边形外的点

##### 其他
```sql
SELECT id,name,lng, lat, ST_GeoHash ( lng, lat, 9 ) AS gh FROM spider_house where id > 0 HAVING gh like 'ww0t%'
```
##### 最终使用的语句，最大lat,lng、最小lat,lng
```sql
SELECT
	id,
	NAME,
	lng,
	lat,
	ST_GeomFromText ( 'POLYGON((113.6072156230005 34.91586596173386,113.6072156230005 34.88135338391958,113.629493599648 34.88135338391958,113.629493599648 34.91586596173386,113.6072156230005 34.91586596173386))' ) AS ste,
	Point ( lng, lat) AS rpt 
FROM
	spider_house 
WHERE
	id > 0 
HAVING
	st_contains ( ste, rpt ) = 1
```

#### mysql 获取两点之间的距离
```sql
SELECT subway_id, name, city_id, parent_id, lng, lat, (st_distance_here ( point ( 119.335745, 26.148543 ), point ( lng, lat ) )) * 111.195 AS distance FROM subway WHERE city_id = 350100 AND parent_id > 0 HAVING distance <= 1.5 ORDER BY distance ASC
```


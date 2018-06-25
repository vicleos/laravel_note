- Solution 1:  修改1列
```mysql
update student s, city c
set s.city_name = c.name
where s.city_code = c.code;
```
- Solution 2:  修改多个列
```mysql
update  a,  b
set a.title=b.title, a.name=b.name
where a.id=b.id
```
- Solution 3: 采用子查询
```mysql
update student s set city_name = (select name from city where code = s.city_code);
```

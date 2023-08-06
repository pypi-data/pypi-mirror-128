##### 使用前，请在taos客户端创建数据库：CREATE DATABASE IF NOT EXISTS test;
##### 必须指定database；pool_size指定连接池大小，是可选的，默认是1，可以根据需要设置大小
##### tz_offset默认是东八区：8
##### 本例使用客户端taos.cfg配置，其它参数请参照taos.connect()方法，初始化后，项目里到处都可以用了
```
td.init_db(database="test", pool_size=2, tz_offset=8)
```
##### 创建stable
```
td.execute("CREATE STABLE IF NOT EXISTS meters(ts timestamp, current float, voltage float, phase int) TAGS(location nchar(20), groupId tinyint)")
```
##### 往单表插入一条数据，如果表不存在就先创建表，必须指定tags，如本例中的'location'和'groupId'
```
td.insert_one_with_stable(table='meter_01', stable='meters', ts=datetime.now(), current=0.2550, voltage=0.3542, phase=0, location='北京', groupId=0)
```
##### 往单表插入一条数据，表已经存在, 可以直接插入，不需要指定 stable和tags
```
td.insert_one(table='meter_01', ts=datetime.now()-timedelta(minutes=10), current=0.3550, voltage=0.5542, phase=1)
```
##### 往单张表插入多条记录
```
meters = [
    {"ts": datetime.now() - timedelta(minutes=1), "current": 0.3550, "voltage": 0.5542, "phase": 2},
    {"ts": datetime.now() + timedelta(hours=1), "current": 0.3550, "voltage": 0.5542, "phase": 3},
]
td.insert_many(table='meter_01', args=meters)
```
##### 往单张表插入多条记录， 如果表不存在，就创建表
```
meters = [
    {"ts": "2021-11-19 15:30:44.123445", "current": 0.3550, "voltage": 0.5542, "phase": 0, "location": "上海", "groupId": 1},
    {"ts": datetime.now() - timedelta(hours=1), "current": 0.3550, "voltage": 0.5542, "phase": 1, "location": "上海", "groupId": 1},
]
td.insert_many_with_stable(table='meter_02', stable="meters", args=meters)
```
##### 同时往多张表插入记录, 'meter_01', 'meter_02'表已经存在，可以不加stable；'meter_03'必须指定stable
```
meters = [
    {"table": "meter_01", "ts": "2021-11-19 17:30:43.1234", "current": 0.3550, "voltage": 0.5542, "phase": 4, "location": "北京", "groupId": 0},
    {"table": "meter_02", "ts": "2021-11-19 17:30:43.1234", "current": 0.3550, "voltage": 0.5542, "phase": 2, "location": "上海", "groupId": 1},
    {"table": "meter_03", "stable": "meters", "ts": datetime.now(), "current": 0.3550, "voltage": 0.5542, "phase": 0, "location": "天津", "groupId": 2},
]
td.insert_many_tables(args=meters)
```
##### 查询表中行数
```
count = td.get("select count(1) from meters")
```
##### 查询单值
```
last_current = td.get("select last(current) from meters")
```
##### 查询一行
```
last_row = td.select_one("select last_row(*) from meters")
```
##### 查询 list
```
bj_rows = td.select("select * from meters where location = '北京'")
```
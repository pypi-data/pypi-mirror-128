# Sqlee
基于Gitee API搭建的数据存储系统.
## 安装
`pip install sqlee`

## 使用
### 连接Gitee数据库
你可以使用以下代码来创建一个新的数据库实例：
```python
import sqlee

db = sqlee.connect(
        access_token = "你的Gitee API Token",
        owner = "你的Gitee用户名",
        repo = "你的数据库名",
    )

```
### 创建表
```python
db.objects.create(name="表名")
```

### 删除表
```python
db.objects.delete(name="表名")
```

### 读取表
```python
db.objects.all() #读取所有表(同时捕获所有数据)
db.objects.get(name="实例表名") #读取指定数据表(同时捕获该表所有数据)
```

### 数据库操作
```python
table = db.objects.get(name="实例表名")
table.objects.all() #读取全部的数据
table.objects.create(datas=(1, 2)) #创建新的数据
table.objects.get(id=0) #读取第0个数据
table.objects.get(id=0).delete() #删除第0个数据
```

### 命令行
`db.interact()`

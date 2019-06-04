# 记录本地的辅助工具


### 建立触发器重建告警日志的表格。请求参数都不变。


```bash
docker run -d -p 27017:27017 --name mongo \
    -v $(pwd)/mongod.conf.orig:/etc/mongod.conf.orig \
    -v /srv/docker/mongo_data:/data -e MONGO_INITDB_ROOT_USERNAME=root \
    -e MONGO_INITDB_ROOT_PASSWORD=test@1q2w2e4R \
    mongo
```

紧接着执行对应的数据库， 进去之后创建对应的远程连接角色。

[docker-mongo配置说明](../../__dev/fluentd/readme.md)

## 创建指定数据库的管理用户。

```
db.createUser({user:"admin007",pwd:"myadmin@816", roles: [ { role: "dbAdmin", db: "logs" }]})
```
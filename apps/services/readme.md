# xxscan 中的审计和安全模块。可以放弃


# 相关接口使用教程 [2018-7-19]


## Curl 命令获取文件
- [CURL 教程](http://man.linuxde.net/curl)
- curl http://localhost:3322/waf/mg/setup-common-conf -o crs-setup-example.conf.bak --progress 
- curl http://localhost:3322/waf/mg/get_prules_txt -o get_prules_txt.conf.bak --progress 

## 当前处理思路；
- waf 开启的规则是用户输入的表单写入到 Mongo
- 继续上面一步, 用户操作的数据和 mysql 串联
- 用户自定义规则写入到本地的 Mysql 记录便于管理

## 后续要进行的内容
- 1, 定时重启 waf, 使对应的 waf 规则生效， 备份和监听
- 2, 格式化 subprocess 的输出; 监听
- 3, 升级和使用新的 waf 文件。

### 改进
- 实验选中当前的规则和远程重启 waf;
- 实验开启配置和重启 waf;

## web_前端（F:\test222222）


## 2018-8-1 
- 数据库迁移，全部采用 WAF 设备上的数据库;
- 删除 `migrations` 重新配置，再重新导入数据库表格
- 执行 `python manage.py migrate --fake`


## 2018-8-10
- 数据库存储 `phaser1_8_10.sql`
- 多对多数据库注意事项参考;先save, 再Add; 防止数据库没有示例添加
- [Django官网解决](https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/) ,
 [StackOverFlow 解决](https://stackoverflow.com/questions/7837033/valueerror-cannot-add-instance-is-on-database-default-value-is-on-databas/7999014)
 
 
## 2018-8-11
- 准备工作：开始准备让 AccessLog 的日志进入数据库
- 准备工作：开始准备让 modsec_auditlog 的数据进入数据库


## 2018-8-13 
- 删除没用的表; 已经被 phaser1/RuleTxt2 取代

```
# Create your models here.
# class RuleFileTemplates(models.Model):
#     rule_file = models.CharField(u"规则文件名", max_length=155, default="57215721")
#     rule_content = models.TextField(u"规则内容")

# class WafRule(models.Model):
#     rule_id = models.IntegerField(u"规则的ID")
#     rule_line = models.CharField(u"文件中所在行", max_length=55, default="0.0.0.0")
#     rule_file = models.CharField(u"规则的文件名", max_length=255,  default="")
#     rule_msg = models.CharField(u"告警消息", max_length=255,  default="")
#     rule_msg_cn = models.CharField(u"中文告警信息", max_length=255,  default="")
#     rule_desc = models.CharField(u"简易描述",max_length=155, default="")
#     # rule_slug = models.TextField(u"指向的位置",max_length=255, default="")
#     # rule_belong = models.TextField(u"指向的位置",max_length=255, default="/etc/")
#     rule_categary = models.CharField(u"规则分类", max_length=55, default="")
#     rule_extra = models.CharField(u"备注", max_length=155, default="")
#
#     # http_x_forwarded_for=http_x_forwarded_for,
#
#     class Meta:
#         verbose_name = u"WAF规则大全和描述（CSR-Setup自带的）"

#
# class WafSetConfig(models.Model):
#     remote_addr = models.CharField(u"请求IP",max_length=55, default="0.0.0.0")
#     remote_user = models.CharField(u"用户",max_length=255,  default="")
#
# class UserOpreation(models.Model):
#     opreation = models.CharField(u"操作", max_length=255, default="")
```

## 2018-8-16
- 必须完成系统中删除规则文件启停的设置文件
- `-`

## 2018-8-27
-  `https://blog.csdn.net/wang785994599/article/details/80896296`

## 2018-9-10
- 为了方便性, 基于后台默认的用户系统; 扩展用户和用户组
- 增加用户操作说明和保护接口的编写
- 完善操作流程的逻辑 (修改规则和重启)
- 完善接口文档的前台显示; `parse_to` 和 `urllib` 使用
  - 1, 当用户访问对应的接口, 后台自动进行记录和写入日志db, 后续版本用异步进行处理。
  - 2, 针对接口做一个接口文档(前台展示的URL永远不爆露, 进行token跳变)。
  - 3, 根据访问的接口和接口文档联立。
- [详细转到](../api/readme.md)

## 2018-9-11
- 修改 `opt` 中高级规则管理。 [详细](./api/opt/readme.md)
- 修改 `oauth` 用户认证, 支持黑白名单, 登陆用户的证书管理

## 2018-9-12
- 放弃 `wafmanage` 目录下除了 `.models.py`， `urls.py`, `api`, `utils` 目录之外的所有文件。
- 其他文件都已经失效, [新工作环境](./api/readme.md)

## 2018-9-13
- 重复上面的叙述，让7月份的链接和数据库表格全部失效
- 编辑urls失效即可

## 2018-10-15 安排
- 利用`subprocess`模块控制 `waf` 引擎
- [subprocess实例](./dprocess.py)
- 完成以下功能
  - a, 引擎重启 [1]
  - b, 规则替换原始的规则  [1]
  - c, 替换失败和重启
  - d, 设置防盗链 referer
  - e, 设置错误模板的上传接口和相关处理逻辑  [1]
  - f, 设置历史accsslog里面根据输入时间段搜索得到20个访问考前的IP


## a 引擎重启
- `service nginx restart`
- `nginx -s reload`

## b 替换之前的规则
- [配置文件](./api/plat/configs/config.ini)

## d ORM/API
- 设置 `serilize.py/viewset` 来控制`phaser1`里面的 ORM表格 `NotEffectReferer` 
- 同时设置 `phaser1` models 里面的引擎 的ORM对象管理等
- 参考 `wafmanage/api/opt` 里面的内容

## f 搜索历史
```sql
select remote_addr, count(remote_addr) as cc \
 from  phaser1_apacheaccesslogdetail  where time_local BETWEEN '2018-2-3' and '2018-5-2' group by remote_addr \ 
order by cc desc limit 20;
```

## waf请求头字段
- [Header头](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers)


## 2019-3-19
- 只保留部分关于 plat 重启的相关接口; 后台简化了，但是让前台知道。
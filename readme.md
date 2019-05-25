# [XX-Scan](https://github.com/xx-scan/xx-scan)

**高并发任务集成扫描器**

## 设计思想

参考[Celerystalk](https://github.com/sethsec/celerystalk)

- 1, 先用Nmap/Nessus/Openvas扫描出结果,再将结果全部存储到XML文件
- 2, 通过XML文件导入进行分析, 生成对应的多Host多服务Services的信息
  - 目前的扫描主要是主机和端口的服务扫描; 无端口的服务(eg:ICMP)暂时不支持
- 3, 根据扫描出来的结果对应什么协议再进行深入的下一步扫描
  - 对应的http/snmp/ssh协议都按照对应的设置的扫描脚本进行.
  - 每个协议可能对应多种扫描器同时扫描
  - 扫描配置参考 [config.ini](./apps/scan/config.ini)
- 4, 当前只是进行扫描器扫描和输出对应的结果文本存储;后面调用actone截图获取对应的网页页面。


## 2019-5-23 
- 创建本项目。并添加了ORM关系和基本的逻辑实现。

## 2019-5-24
> 创建ORM并且进行实验。
- [表格字段说明](./apps/scan/readme.md)
- 流程已经全部跑通

## 2019-5-25
- 增加扫描器的声明; 增加了服务的记录不删除旧的。重新修改了ORM;
- 增加了flower的验证 [flower-auth](https://flower.readthedocs.io/en/latest/auth.html#http-basic-authentication)
- 修改了处理逻辑没有那么多 delete 了。



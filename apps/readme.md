# 2019-6-19
- 1, 修改具体的策略指向的具体内容，优化表格的设计。
- 2, 修改部分关于监控的内容，策略，审计。


## 2019-6-19
- 1, 需要修改chk/audit变更和审计的用户名的存储，以及审计事件添加的表格。
- 2, 需要增加和完善处理逻辑, 修改对应的接入客户端的脚本。
- 3, 平台提供客户端接入的URL, 加密和解密传入数据即可。
- 4, 客户端的运行, 依赖于服务端传给过去的字段预先记录。
 
## 2019-6-26
- 注意事项, 1审计对象, 2安全机制。
- 全部改写 Xadmin 跟测试文档一样。

## 2019-7-2
- 补充很多结构, 存在重大的问题。很多内容都没有细化到具体的进程。
- 注意: 一旦要重写首页抛弃原来的首页结构，使用中间件强制跳转即可。
- [github表情](https://www.jianshu.com/p/bb26733da917)

## 2017-7-3 
- 结构更改和全局使用的设置。
- 全部结构使用。
- 修改这个核心结构为 mgsd `manager-server-d` 


## 2019-7-9
- 1, 开始捕获对象变更和变更进入审计的流程; 主要是对象变更和接入，策略变更等。
- 2, 今天先完成对象变更的内容，关于策略录入和策略下发等，明天再弄。
  - 步骤: 首选进行对象变更和接入。统计所有Log里面关于对象变更的内容; 取出来需要的内容进行过滤。
  - 步骤: 接着增加一列, 是否手动修改进入响应处置。

## 2019-7-11
- 今天出现了权限异常的问题; 无法一对一的获取。permission_group 视图。
- 仍然没有解决的问题是策略管理的优化。
- [git表情大全](https://github.com/liuchengxu/git-commit-emoji-cn)


## 2019-7-12 
- iptabels 设置端口访问
- 故障
```bash 
iptables -t filter -I INPUT -p tcp --dport 18077 -j DROP
iptables -t filter -I INPUT -s 192.168.2.161 -p tcp --dport 18077 -j ACCEPT
iptables -A INPUT -m iprange --src-range 192.168.2.161-192.168.2.255 -j ACCEPT 
```

## 2019-7-15
- 增加部件信息监控总览; 
  - 基于prometheus、snmp进行管理和加载重要进程以及系统的使用。
- 增加部件策略信息加载和设置的总览
- [prometheus中文指导手册](https://yunlzheng.gitbook.io/prometheus-book/introduction)

## 2019-7-19
- 放弃本xadmin使用django-vue
- [xpm-ui](https://github.com/xx-work/xpm-ui)

## 2019-7-22
- 1, 放弃所有的vue-admin 
  - 1, 因为新版本的CSO 前台要对接经典的; 所以放弃。
  - 2, 有点复杂

## 2019-8-1
- 新库 `cso81`
- [初始化详情](./mgsd/xint/2019_06_18_inital_eventinfo.py)
- [初始化IPS/SCAN](./agent/tests/2019_08_01_tset_scan_coper_and_api.py)
- [初始化POT](./mgsd/xint/2019_07_14_inital_pot_infos.py)

## 2019-8-7
- SNMP trap 了解和拓展学习; 方便监控告警.
  - 发现不太好弄; 解决方法是，在两台机器上搭建一个使用psutil的服务即可。将数据发送到
  - https://www.home-assistant.io/docs/installation/ 所以基于上面的状态获取实时的数据展示
    - [home-assistant](https://www.home-assistant.io/docs/) 使用这个开源监控的数据框架.
    - osquery, angeti 都是以后的事儿。

## 2019-8-13
- 创建 Tornado-Django 共存器; 一部分处理Django-一部分处理Tornado应用。
- [参考codo-cron](https://github.com/opendevops-cn/codo-cron)
- [APP开始后从本地的Redis加载基本的信息](./agent/api/cache_loads.py)
- 注意安装 依赖，[requirements.txt](./ops/libs/requirements.txt)

## 2019-8-16
- 开始移植 ops 到xx-scan 开发第二代xx-scan，重大更新下。
- 使用工作中使用到的任务监督管理工具[ops-sdk](./ops)。
> 关于 secs和ops 后期都会打包成 django-app 作为SDK使用。
- 关于新版本的使用后面再说。
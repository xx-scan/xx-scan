## 开发表格设计说明

```python 
from .host import Host, Service
from .scan_cfg import ScanTool, Scheme, ScanRecode, NmapServiceName, Protocol
from .report import ReportFormat, ScanReport
from .task import ScanTask
```

- Workspace
> 扫描空间

- Host
> 对应的表格为主机信息表，比如主机的厂商，mac, ip 信息等。

- Service
> 对应Nmap扫描出来的服务表

- ServicePort
> 常用的端口

- NmapServiceName
> 对应的是Nmap扫描的服务名的集合; 和协议对应。

- ScanTool
> 对应的是扫描工具的表

- ScanScript
> 对应的是扫描脚本表

- Scheme
> 对应的是扫描方案的表格

- ScanRecode
> 对应的是扫描记录的表格

- ScanReport 
> 对应的是扫描报告的表格

- ReportFormat
> 对应的是扫描格式化的表格

- ScanTask
> 对应的是扫描定时任务的表格

## Workspace 个人空间创建【2019-6-2】
- 任何一个方案，一个预扫描过程都要独立出来，其他的空间进行读了，需要才参考。
- 这个思想类似, metasploit-framework 中的workspace同样也类似于 `celerystalk`中。
- **思路**
  - 每一个Host，Service, ScanCode 都会返回去一个WorkSpace，
  - 所以扫描过程中，新增的主机，服务，结果必须返回给对应的空间内容。
  - 当前思想，任何一个连贯性，或者探测发现阶段的任务都需需要定制。定制的内容包括了用户空间。
  - 用户空间中包含了用户自定义的扫描方案，ScanRecode的记录要依赖于用户空间

## OpenVas Scan Add (openvas)

## Vuls Scan Add (vuls)


## 2019-6-6
- 借助 masscan 扫描出端口和主机, 接着进行Nmap服务扫描。
- 由于部署环境下的网卡不是 IntelXL/Intel8000x 系列，所以没有加速环境。不进行扫描。
- 只提供masscan扫描结果的json文本导入到平台中，再进行二次扫描。
- [Code_Location](./api/mudules/scan_v2/upgrade/masscan.py)

## 2019-6-9
- 增加平台的告警消息。主要记录平台中扫描器设置相关的问题。
- [CodeLocation](./models/audit.py) 当前未注册
- 上面的平台告警信息, 已经移动到 services 中 的 `PlatHistory`

## 2019-6-11
- 1, WorkSpace-Form在xadmin的ScanTask-StepForm中不能完美兼容，后期修改为Raw;
- 2, 产生文本并记录。chain到环境上。或者手动更新到页面【推荐】。




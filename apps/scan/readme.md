## 开发表格设计说明

```python 
from .host import Host, Service
from .scan_cfg import ScanTool, Scheme, ScanRecode, NmapServiceName, Protocol
from .report import ReportFormat, ScanReport
from .task import ScanTask
```

- Host
> 对应的表格为主机信息表，比如主机的厂商，mac, ip 信息等。

- Service
> 对应Nmap扫描出来的服务表

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

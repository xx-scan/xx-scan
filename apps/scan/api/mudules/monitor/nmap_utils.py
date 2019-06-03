from libnmap.parser import NmapParser
# import uuid

from ....utils.ltool.utils.dt_tool import get_pydt_based_logdt, get_pydt2_based_nmap
from ....models import Host, Service

path = "F:\\workspace\\xx-scan\\apps\\scan\\datas\\nmap_results\\sV.xml"

FilterByIp = True


def get_current_host(_host):
    _ip = _host.id
    _mac = _host.mac
    _vendor = _host.vendor
    _filters = Host.objects.filter(mac=_mac)
    if FilterByIp:
        _filters = Host.objects.filter(ip=_ip)
    if len(_filters) > 0:
        host = _filters[0]
    else:
        host = Host(name=_ip,ip=_ip,type="自发现设备",os="-",mac=_mac,mac_vendor=_vendor,up=True,)
        host.save()
    return dict(host=host, ip=_host.id, mac = _host.mac,  vendor= _host.vendor, )


def get_needs_datas_from_xmlpath(xml_path=path, incomplete=False):
    nmap_report = NmapParser.parse_fromfile(xml_path, incomplete=incomplete)
    # 主机存活验证
    judge_hosts_survived(nmap_report)

    _time = get_pydt2_based_nmap(nmap_report._runstats["finished"]["timestr"])
    _services_list = []
    for _host in nmap_report.hosts:
        _host_info = get_current_host(_host)
        host = _host_info["host"]
        for _service in _host.services:
            service = _service.get_dict()
            if service["service"] in ["tcpwrapped", ]:
                continue
            del service["id"]
            _services_list.append( Service(**service, descover_time=_time, host=host), )
    Service.objects.bulk_create(_services_list)


def judge_hosts_survived(nmap_report):
    # _time = get_pydt2_based_nmap(nmap_report._runstats["finished"]["timestr"])
    _services_list = []
    survived_hosts = [_host.id for _host in nmap_report.hosts ]
    for host in Host.objects.all():
        _up = host.up ## 之前的状态
        if host.ip in survived_hosts:
            if _up == True:
                continue
            host.up = True
        else:
            if _up == False:
                continue
            host.up = False
        host.save()

    for service in Service.objects.all():
        _up = service.running
        if service.host.ip in survived_hosts:
            if _up == True:
                continue
            service.running = True
        else:
            if _up == False:
                continue
            service.running = False
        service.save()

    from ....models import ScanRecode
    for recode in ScanRecode.objects.all():
        _up = recode.active
        if recode.target in survived_hosts:
            if _up == True:
                continue
            recode.active=True
        else:
            if _up == False:
                continue
            recode.active=False
        recode.save()
    ## 主机, 服务, 运行的记录


SURVIVE_MONITOR_CACHE_KEY = "SURVIVE_MONITOR_CACHE_KEY"


def hosts_survice_monitor(xml_path=path, incomplete=False):
    """
    最大范围行的存活性检测; 检测完毕之后进行入库。存活主机的扫描。
    :param xml_path: nmap -sP -PR -sn <targets> -oX <xml_path>
    :param incomplete: 中途写入
    :return:
    """
    nmap_report = NmapParser.parse_fromfile(xml_path, incomplete=incomplete)
    # 主机存活验证
    judge_hosts_survived(nmap_report)

    _time = get_pydt2_based_nmap(nmap_report._runstats["finished"]["timestr"])
    _services_list = []
    survived_hosts = []
    for _host in nmap_report.hosts:
        _host_info = get_current_host(_host)
        survived_hosts.append(_host_info["host"])

    for host in Host.objects.all():
        _up = host.ip
        if host in survived_hosts:
            if _up == True:
                continue
            host.up = True
        else:
            if _up == False:
                continue
            host.up = False

    from django.core.cache import cache

    ## 存活主机加入外键
    cache.set(SURVIVE_MONITOR_CACHE_KEY, [x.ip for x in Host.objects.filter(up=True)])



















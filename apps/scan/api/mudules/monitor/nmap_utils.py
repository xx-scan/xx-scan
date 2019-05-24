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


def get_needs_datas_from_xmlpath(xml_path=path, incomplete=False, DEBUG=False):
    nmap_report = NmapParser.parse_fromfile(xml_path, incomplete=incomplete)
    _time = get_pydt2_based_nmap(nmap_report._runstats["finished"]["timestr"])
    # print(_time)
    _services_list = []
    if not DEBUG:
        Service.objects.all().delete()

    for _host in nmap_report.hosts:
        _host_info = get_current_host(_host)
        # ip = _host_info["ip"]
        host = _host_info["host"]
        for _service in _host.services:
            service = _service.get_dict()
            if service["service"] in ["tcpwrapped", ]:
                continue
            del service["id"]
            _services_list.append( Service(**service, descover_time=_time, host=host), )

    if not DEBUG:
        Service.objects.bulk_create(_services_list)




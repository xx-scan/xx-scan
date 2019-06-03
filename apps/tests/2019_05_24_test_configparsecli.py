import os
import sys

from src import django_setup

def test():
    django_setup()
    from scan.api.mudules.scan_v2.prepare.put_default_2cfg import orm_delete, inital_scan_cfgs, inintal_services, inital_scheme, inital_scan_tools
    orm_delete()
    inital_scan_cfgs()


def test_discover():
    django_setup()
    _path = "F:\\workspace\\CSO\\apps\\cso\\datas\\nmap_results\\sV.xml"
    from scan.api.mudules.monitor.nmap_utils import get_needs_datas_from_xmlpath
    get_needs_datas_from_xmlpath("F:\\workspace\\xx-scan\\data\\sV.xml")


def test_recode():
    django_setup()

    from scan.api.mudules.scan_v2.recode import collect_recodes
    collect_recodes()


def common_ports():
    with open("F:\\xx-scan\\data\\ports.txt", "r", encoding="utf-8") as f:
        string = f.read()
        f.close()
    import re
    datas = re.findall("<tr>(.*?)</tr>", string)

    _results = []
    for x in datas:
        print(x)
        _tds = re.findall("<td>(.*?)</td>", x)
        if len(_tds) > 3:
            _results.append({
                "port_info": _tds[0],
                "desc": _tds[1],
                "official": _tds[2]
            })
    for x in _results:
        print(x["port_info"])



if __name__ == '__main__':
    test()
    #test_discover()
    #test_recode()

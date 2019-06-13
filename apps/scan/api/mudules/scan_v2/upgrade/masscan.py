# coding:utf-8

# masscan 扫描出来的结果放置到REDIS, 接着再从redis获取信息进行Namp服务探测。不放入到数据库
import re, os
import json
from django.core.cache import cache

"""
masscan -p65525 104.18.2.0-104.18.5.255 --rate=1000 --open --banners  -oJ local.json 
"""

from website.settings import PROJECT_DIR
default_demo_json_path = os.path.join(PROJECT_DIR, "apps", "scan", "api", "mudules", "scan_v2", "tmp", "ms.json")

def msjson2cache(json_path=default_demo_json_path):
    """
    将Masscan扫描出来的 hosts,ports 结果存储到缓存中，给Nmap进行基础扫描。
    :param json_path: masscan 导出的json路径
    :return:
    """
    with open(json_path, 'r', encoding="utf-8") as f:
        ms_txt = f.readlines()
        f.close()

    # 导出结果后进行; 将targets和ports聚类
    ips, ports = [], []

    for line in ms_txt:
        matched = re.match(".*?ip\: \"(\d+\.\d+\.\d+\.\d+)\",.*?port: (\d+),.*", line)
        if matched:
            ips.append(matched.group(1))
            ports.append(matched.group(2))

    return dict(
        ports=set(ports),
        targets=set(ips),
    )

def masscan_results_continue():
    from scan.models import ScanTask

    # 2019-6-11 感觉用处不大，准备创建 masscan 上传的视图进行后续ScanTask扫描，但是不用了。

    pass
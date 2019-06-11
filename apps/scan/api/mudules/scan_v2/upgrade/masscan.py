# coding:utf-8

# masscan 扫描出来的结果放置到REDIS, 接着再从redis获取信息进行Namp服务探测。不放入到数据库

from django.core.cache import cache


def msjson2cache(json_path):


    return dict(
        ports="",
        targets="",
    )
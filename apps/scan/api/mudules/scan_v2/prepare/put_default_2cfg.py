# coding:utf-8
import os
import re
from configparser import ConfigParser
from django.contrib.auth.models import User
from website.settings import PROJECT_DIR


SCAN_CONFIG_FILE = os.path.join(PROJECT_DIR, "apps", "scan", "config.ini")

from .....models import Protocol, NmapServiceName, ScanScript, Scheme, Workspace


def orm_delete():

    Workspace.objects.all().delete()

    Scheme.objects.all().delete()
    ScanScript.objects.all().delete()
    NmapServiceName.objects.all().delete()
    Protocol.objects.all().delete()

    User.objects.all().delete()
    create_default_user_and_workspace()


def get_default_superuser():
    try:
        superuser = User(username="admin", password="admin",
                            email="test@example.com",
                            is_superuser=True, is_staff=True, is_active=True)
        superuser.set_password("admin")
        superuser.save()
    except:
        superuser = User.objects.filter(username="admin")[0]
    return superuser


def create_default_user_and_workspace():
    superuser = get_default_superuser()

    Workspace.objects.create(
        user=superuser,
        name="xadmin"
    )


def inintal_services(config_file=SCAN_CONFIG_FILE, inintal=True, add_many=True):
    if inintal:
        Protocol.objects.all().delete()
        NmapServiceName.objects.all().delete()

    config = ConfigParser(allow_no_value=True)
    config.read([config_file])

    supported_services = []
    for (protocol, val) in config.items("nmap-service-names"):
        services = val.split(",")
        _protocol, _slug = Protocol.objects.get_or_create(protocol=protocol)
        # supported_protocols.append(_protocol)
        for servicename in services:
            if len(NmapServiceName.objects.filter(protocol=_protocol, service_name=servicename)) > 0:
                continue
            service = NmapServiceName(protocol=_protocol, service_name=servicename)
            supported_services.append(service)
            if not add_many:
                try:
                    service.save()
                except:
                    _info = "操作[" + servicename + "]到数据库失败！"
                    try:
                        from services.models import PlatOptHistory
                        PlatOptHistory.objects.create(desc=_info)
                    except:
                        import logging
                        logging.error(_info)
    if add_many:
        try:
            NmapServiceName.objects.bulk_create(supported_services)
        except:
            # 多条同时插入插入失败的情况下就用这个。
            inintal_services(add_many=False)


def inital_scan_tools():
    ScanScript.objects.all().delete()

    config = ConfigParser(allow_no_value=True)
    config.read([SCAN_CONFIG_FILE])
    
    scan_tools = []
    supported_protocols = Protocol.objects.all()
    for protocol in supported_protocols:
        for (name, used_script) in config.items(protocol.protocol):

            args = ",".join(re.findall("\[(.*?)\]", used_script))
            _scan_tool = ScanScript(name=name, used_script=used_script, args=args, protocol=protocol)
            scan_tools.append(_scan_tool)
    ScanScript.objects.bulk_create(scan_tools)


def inital_scheme():
    """
    当前实验只有Nmap脚本的示例
    :return:
    """
    Scheme.objects.all().delete()

    scheme_nmap = Scheme(name="scheme_nmap", desc="Nmap方案", create_user=get_default_superuser())
    scheme_all = Scheme(name="scheme_all", desc="所有扫描配置的方案", create_user=get_default_superuser())

    scheme_nmap.save()
    scheme_all.save()

    for x in ScanScript.objects.all():
        have_installed_tools = ["nmap", ]
        _tool_sets = "|".join(have_installed_tools)
        matched = re.match("^({}).*?".format(_tool_sets), x.used_script)
        scheme_all.scan_tools.add(x)
        if matched:
            scheme_nmap.scan_tools.add(x)


def inital_scan_cfgs(config_file=SCAN_CONFIG_FILE):
    #orm_delete()

    inintal_services(config_file=config_file)
    inital_scan_tools()
    inital_scheme()

    import logging
    logging.warning("初始化完成")

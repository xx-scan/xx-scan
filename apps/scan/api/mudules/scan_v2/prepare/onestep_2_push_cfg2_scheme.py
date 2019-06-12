# coding:utf-8
import re
import uuid
from configparser import ConfigParser
from scan.models import Protocol, ScanScript, Scheme
from .put_default_2cfg import inintal_services


def push_cfg_2_scheme_in_one_step(cfg_path, scheme_name=str(uuid.uuid4()), scheme_desc=''):
    """
    一步将cfg文本中的内容转化为方案。 这里的cfg_path 内容就是 scan/config.ini 中格式相近
    :param cfg_path:
    :return:
    """
    # 先加载服务名称到平台中存储
    inintal_services(config_file=cfg_path, inintal=False, add_many=False)

    config = ConfigParser(allow_no_value=True)
    config.read([cfg_path])

    scan_tools = []
    supported_protocols = Protocol.objects.all()
    for protocol in supported_protocols:
        try:
            for (name, used_script) in config.items(protocol.protocol):
                args = ",".join(re.findall("\[(.*?)\]", used_script))
                filterd = ScanScript.objects.filter(name=name, used_script=used_script, args=args, protocol=protocol)
                if len(filterd) > 0:
                    scan_tools.append(filterd[0])
                    continue
                _scan_tool = ScanScript.objects.create(name=name, used_script=used_script, args=args, protocol=protocol)
                scan_tools.append(_scan_tool)
        except:
            import logging
            logging.error(protocol.protocol + ": 异常")

    ## 工具已经导入了, 开始指定加载的方案;
    from django.contrib.auth.models import User
    _scheme = Scheme(name=scheme_name, desc=scheme_desc, create_user=User.objects.get(username="admin"))

    ## 能不能在这里调用 Xadmin 的 save_model; 这里可以放置; 只有某些用户能导入。


    _scheme.save()
    for x in scan_tools:
        _scheme.scan_tools.add(x)

    try:
        from services.models import PlatOptHistory
        PlatOptHistory.objects.create(
            desc="导入扫描方案配置",
            opreatername="script",
            extra = "scheme_name"
        )
    except:
        # Alert
        pass


def export(instance):
    """
    导出方案; 导出方案为 config.ini 格式的文件。
    :param instance:
    :return:
    """
    pass
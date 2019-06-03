import uuid
from django.db import models


class ServicePort(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    port = models.IntegerField(verbose_name="端口数值")
    port_name = models.CharField(verbose_name="端口名称", blank=True, max_length=255)
    desc = models.CharField(verbose_name="端口描述", blank=True, max_length=255)
    type = models.CharField(verbose_name="类型", blank=True, max_length=255)
    type_desc = models.CharField(verbose_name="类型描述", blank=True, max_length=255)
    protocol = models.CharField(verbose_name="传输层协议", default="tcp", max_length=30)
    # official = models.BooleanField(verbose_name="官方", default=True)
    # date_created = models.DateTimeField(auto_now_add=True)
    # date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.port


def inital_ports():
    import re
    from scan.utils.ltool.port_data import port_data

    for x in port_data["data"]:

        port_info = x["port"]

        matched_sigle = re.match("(\d+)/(\w+)\s*", port_info)
        protocol = ""
        if matched_sigle:
            port = int(matched_sigle.group(1))
            protocol = matched_sigle.group(2)
        else:
            matched_num = re.match("(\d+)\s*", port_info )
            if matched_num:
                port = int(matched_num.group(1))
                protocol = "unknown"
            else:
                print(port_info)
                continue
        if protocol == "unknown":
            ServicePort.objects.create(
                port=port,
                port_name=x["portname"],
                desc=x["desc"],
                type=x["type"],
                type_desc=x["type_desc"],
                protocol="tcp"
            )
            ServicePort.objects.create(
                port=port,
                port_name=x["portname"],
                desc=x["desc"],
                type=x["type"],
                type_desc=x["type_desc"],
                protocol="udp"
            )
            continue

        ServicePort.objects.create(
            port=port,
            port_name=x["portname"],
            desc=x["desc"],
            type=x["type"],
            type_desc=x["type_desc"],
            protocol=protocol
        )



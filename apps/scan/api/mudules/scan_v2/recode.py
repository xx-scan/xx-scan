from ....models import ScanReport, ScanRecode, Service, Protocol, Scheme, NmapServiceName

UNSERV = "_unserv"
DEFAULT_SCHEME = Scheme.objects.filter(name="scheme_nmap")[0]

def get_scan_plan_based_scheme_and_service(service, scheme_id=DEFAULT_SCHEME.id):
    target = service.host.ip
    port = service.port
    service_name = service.service
    try:
        protocol = NmapServiceName.objects.filter(service_name=service_name)[0].protocol
    except:
        _unserv, _slug = Protocol.objects.get_or_create(protocol=UNSERV)
        print(service_name +"没有注册服务")
        NmapServiceName.objects.get_or_create(service_name=service_name, protocol=_unserv)
        return None
    path = "/robot.txt"
    scan_recodes = []

    _selected_tools = Scheme.objects.get(id=scheme_id).scan_tools.all()

    for x in _selected_tools:
        if x.protocol == protocol:
            _scheme = ScanRecode(scan_tool=x, target=target, port=port, path=path)
            scan_recodes.append( _scheme )
            # print(_scheme.extract_self())
    return scan_recodes


def collect_recodes():
    ScanRecode.objects.all().delete()
    recodes = []
    for service in Service.objects.all():
        _recodes_part = get_scan_plan_based_scheme_and_service(service=service)
        if _recodes_part:
            recodes.extend(_recodes_part)
    [x.save() for x in recodes]
    # ScanRecode.objects.bulk_create(recodes)
    return recodes






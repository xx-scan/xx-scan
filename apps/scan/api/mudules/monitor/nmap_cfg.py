import os
import uuid

from website.settings import PROJECT_DIR
NmapDataDir = os.path.join(PROJECT_DIR, "datas", "nmap_scan")
if not os.path.exists(NmapDataDir):
    os.makedirs(NmapDataDir)

Nmap_xml_result_path = os.path.join(NmapDataDir, "result_" + str(uuid.uuid4()) + ".xml")
NmapScanDefaultBin = "/usr/bin/nmap"
NmapScanDefaultArgs = "-sS -sV -p1-65535 -O"
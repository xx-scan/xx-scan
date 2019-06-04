import subprocess
import re
from ....models import ScanTool

def judge_bin_soft_in_system(judge_script):
    p = subprocess.Popen(judge_script, shell=True, stdout=subprocess.PIPE)
    _line = p.stdout.read().decode("utf-8").split("\n")
    for line in _line:
        if re.match(".*?command not found*?", line):
            return False
    return True


def load_scripts_state():
    for scan_tool in ScanTool.objects.all():
        if judge_bin_soft_in_system(scan_tool.judge_script):
            scan_tool.in_system = True
            continue
        scan_tool.in_system = False
        scan_tool.save()


def install_script(scan_tool):
    if scan_tool.in_system:
        return {"stat": False, "reason": "【" + scan_tool.name + "】 Have Existed in System"}
    else:
        p = subprocess.Popen(scan_tool.install, shell=True, stdout=subprocess.PIPE)
    return True

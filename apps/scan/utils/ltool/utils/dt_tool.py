from datetime import datetime, timedelta
import re

# 月份键值对
month_kv = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12, )


def get_pydt_based_logdt(logdt_str):
    dt_matched = re.match("(\d+)/(\w+)/(\d+):(\d+):(\d+):(\d+)",  logdt_str)
    if dt_matched:
        dt_kwargs = dict(
            day=int(dt_matched.group(1)),
            month=month_kv[dt_matched.group(2)],
            year=int(dt_matched.group(3)),
            hour=int(dt_matched.group(4)),
            minute=int(dt_matched.group(5)),
            second=int(dt_matched.group(6)),
        )
        return datetime(**dt_kwargs)

def get_pydt2_based_nmap(logdt_str):
    dt_matched = re.match("""\w+ (\w+) (\d+) (\d+):(\d+):(\d+) (\d+)""", logdt_str)
    if dt_matched:
        dt_kwargs = dict(
            day=int(dt_matched.group(2)),
            month=month_kv[dt_matched.group(1)],
            year=int(dt_matched.group(6)),
            hour=int(dt_matched.group(3)),
            minute=int(dt_matched.group(4)),
            second=int(dt_matched.group(5)),
        )
        return datetime(**dt_kwargs)


def get_ua_and_os_from_User_Agent(ua_str):
    # 需要安装这个包的哦
    from ua_parser import user_agent_parser
    up = user_agent_parser.Parse(ua_str)
    return dict(
        user_agent=up["user_agent"]["family"],
        os=up["os"]["family"],
        device=up["device"]["family"]
    )

def get_dt_by_str(dt_str = "2017-08-27 05:00:39"):
    import re
    from datetime import datetime
    parter = "(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+).*?"
    matched = [int(re.match(parter, dt_str).group(i+1)) for i in range(6)]
    return datetime(*matched)

# 优化正则, 无缝衔接； 修复本来存在“.m -_(”等
def re_upgrade_str(content):
    re_partertn_list = list("{}._()-*^+$?")
    _outstr = ""
    for c in re_partertn_list:
        _outstr = content.replace(c, "\\" + c)
    return _outstr
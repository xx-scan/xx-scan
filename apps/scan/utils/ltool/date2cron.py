import re
from datetime import datetime


def change_dt_to_crontab(_datetime):
    """
    # 将 DateTime 的字符串类型或者是时间类型转化为crontab的格式。
    # crontab * * * * *
    :param datetime: 字符串或者是时间类型
    :return: True, Crontab
    """
    if type(_datetime) == str:
        matchend = re.match("(.*?)-(.*?)-(.*?) (.*?):(.*?):(.*?)", _datetime)
        if not matchend:
            return False, "Error: Datetime Str should like 2019-1-2 11:11:12"
        _dt = datetime(*[matchend.group(i+1) for i in range(6)])

    if type(_datetime) == type(datetime.now()):
        _dt = _datetime

    crontab = "{minute} {hour} {day} {month} {week}".format(
        minute=_dt.minute,
        hour=_dt.hour,
        day=_dt.day,
        month=_dt.month,
        week="*", # 不用设置
    )
    return True, crontab


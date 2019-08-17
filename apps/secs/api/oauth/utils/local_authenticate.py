from secs.utils.db_utils import from_sql_get_data
from hashlib import md5
from django.contrib.auth.models import User


def l_authenticate(username, password, **kwargs):
    _sql = """select auth_user.username as username, passwd from userprofile 
    left join auth_user on userprofile.user_id=auth_user.id where username='{username}';""".format(username=username)
    _data = from_sql_get_data(_sql)["data"]
    if len(_data) > 0:
        passwd = _data[0]["passwd"]
        md5_passwd = md5(passwd.encode('utf-8')).hexdigest()
        if md5_passwd == str(password):
            return User.objects.get(username=username)
    return None
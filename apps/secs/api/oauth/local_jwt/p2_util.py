from secs.models import UserAuditLog


class UserManageParams():
    def __init__(self):
        self.user_login_times_len = 5 ## 统计次数
        self.caculate_period = 60     ## 统计周期
        self.banned_long = 60*5       ## 封禁时长


class LoginOpreation():

    def __init__(self, username, ip):
        self.username = username
        self.user_manage = UserManageParams()
        self.ip=ip
        self.url="/waf/mg/jwt_login/"
        self.db_table="user_auditlog"


    def login_faild(self):
        UserAuditLog.objects.create(
            username=self.username,
            ip=self.ip,
            url=self.url,
            status=401
           )

    def login_sucess(self):
        UserAuditLog.objects.create(
            username=self.username,
            ip=self.ip,
            url=self.url,
        )


    def check_stat(self):
        """
        2019-4-29 删除IP关联的这个关系。删除了44行的这个IP内容
        and ip='{ip}'
        :return:
        """
        from secs.utils.db_utils import from_sql_get_data
        _sql = """select * from {db_table} where opreate_time > SUBDATE(now(),interval {ana_time} second) 
        and url='{url}'   and status=401 and username='{username}' limit 10;""".format(db_table=self.db_table,
                                                 url=self.url,
                                                 # ip=self.ip,
                                                 username=self.username,
                                                 ana_time=str(self.user_manage.caculate_period) )
        _datas = from_sql_get_data(_sql)["data"]
        if len(_datas) >= self.user_manage.user_login_times_len:
            return False

        return True



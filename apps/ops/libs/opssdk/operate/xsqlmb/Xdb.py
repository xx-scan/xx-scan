from xsqlmb.src.cfgs.basicConfig import DATABASES


class XdbManager():

    def __init__(self, db_name=DATABASES["default"]["NAME"]):
        self.db_name = db_name

    def _create(self):
        from xsqlmb.src.ltool.sqlconn import sql_action
        sql_action("""CREATE DATABASE {db_name} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;""".format(db_name=self.db_name))
        return True

    def _delete(self):
        from xsqlmb.src.ltool.sqlconn import sql_action
        sql_action("""drop database {db_name};""".format(
            db_name=self.db_name))
        return True

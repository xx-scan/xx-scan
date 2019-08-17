from xsqlmb.src.cfgs.basicConfig import default_charset, \
    default_engine, charset_types, engine_types


class SqlModeClass():

    def __init__(self, table_name, columns, autoid="int", primary_key="id", uniq_key=None, CustomTableConfig=None):
        """
        Mysql表的实体
        :param table_name: 表的名字
        :param columns: 所有列的集合
        :param autoid: 是否开启int主键。
        :param primary_key: 主键
        :param uniq_key: 独特的键
        :param CustomTableConfig: 表格字符集和表引擎设置
        """
        self.sqlmodecolumns = columns
        self.autoid = autoid
        self.primary_key = primary_key
        self.uniq_key = uniq_key
        self.table_name = table_name

        # 下面是自助生成的字符集相关的配置; 一般来说不用指定
        self.charset = default_charset
        self.engine = default_engine
        self.primary_key = "id"

        recover = lambda _default, _keyname, _boundary, _cfg: _default if _cfg[_keyname] not in _boundary else _cfg[
            _keyname]
        if CustomTableConfig:
            if "charset" in CustomTableConfig.keys():
                self.charset = recover(default_charset, "charset", charset_types, CustomTableConfig)
            if "engine" in CustomTableConfig.keys():
                self.engine = recover(default_engine, "engine", engine_types, CustomTableConfig)
            if "primary_key" in CustomTableConfig.keys():
                self.primary_key = CustomTableConfig["primary_key"]


    def _sql_create_str(self):
        """
        数据表创建的SQL语句。
        :return:
        """
        _itemsql = """ CREATE TABLE `{table_name}` (""".format(table_name=self.table_name)
        _itemsql += self.get_columns_strs()
        _itemsql += """PRIMARY KEY (`{primary_key}`) {uniq_key} ) ENGINE={engine} DEFAULT CHARSET={charset};""".format(
            primary_key=self.primary_key,
            engine=self.engine,
            charset=self.charset,
            uniq_key=",KEY wh_logrecord_{key_name} ({key_name})".format(key_name=self.uniq_key) if self.uniq_key else ""
        )
        return _itemsql


    def _create(self):
        from  xsqlmb.src.ltool.sqlconn import sql_action
        sql_action( self._sql_create_str() )

        from  xsqlmb.src.cfgs.logConfig import logging
        logging.warning("创建数据表成功")



    def get_columns_strs(self):
        _columns_strs = """"""
        if self.autoid == "int":
            _columns_strs += """`id` int(11) NOT NULL AUTO_INCREMENT,"""
        for column in self.sqlmodecolumns:
            _columns_strs += column.get_create_str()
        return _columns_strs

    @staticmethod
    def get_demo_model():
        from datetime import datetime
        from  xsqlmb.src.dao.xcolumn import SqlModeColumnClass
        _date_str = str(datetime.now()).replace(".", "_").replace(" ","_").replace("-","_").replace(":","_")
        return SqlModeClass(table_name="test_demo_" + _date_str,
                            columns=[
                                SqlModeColumnClass.get_datetime("CreateTime"),
                                SqlModeColumnClass.get_verchar255("email"),
                                SqlModeColumnClass.get_verchar255("username"),
                                SqlModeColumnClass.get_verchar255("password"),
                                SqlModeColumnClass.get_int11("age"),
                                SqlModeColumnClass(_type="datetime", _limit=None, _default=None, _column_name="date_joined", _null=False)
                            ])
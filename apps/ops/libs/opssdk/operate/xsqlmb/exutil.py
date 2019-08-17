
class MutiTypesInsets2SqlClass():

    def __init__(self, table_name):
        """
        支持多种类型的字符串进行写入到mysql
        :param table_name: 表格名称
        """
        self.table_name = table_name


    def filetype2sql(self, filepath):
        pass


    def arrays2sql(self, array2, columns_order):
        """
        数组对象导入到mysql
        :param array2: 数组就是 Insert into 后面 values ({}) 这个对象
        :param columns_order: 就是 insert into table({``,``}) 里面的对象。
        :return:
        """
        if len(array2) < 1:
            return False, "数据不足插入"
        # if len(array2[0]) != len(columns_order):
        #     return False, "带插入对象数据列不匹配"

        _sql_str_list = []
        for _item in array2:
            _sql_str = "(\'" + "\',\'".join(_item.replace("'", "\\dou") ) + "\')"
            _sql_str_list.append(_sql_str)
        _query_sql = """insert into {table_name}({columns}) values {values_str};""".format(
            values_str=", ".join([str(x) for x in _sql_str_list]),
            table_name=self.table_name,
            columns=columns_order
        )
        try:
            from  xsqlmb.src.ltool.sqlconn import sql_action
            sql_action(_query_sql)

            return len(_sql_str_list)
        except:
            try:
                from  xsqlmb.src.cfgs.logConfig import logging
            except:
                import logging
            logging.info("导入数据库失败！")

            return 0

    def arrays2sql2(self, dict_array, columns_order, keys_list):
        """
        数组对象导入到mysql
        :param array2: 数组就是 Insert into 后面 values ({}) 这个对象
        :param columns_order: 就是 insert into table({``,``}) 里面的对象。
        :param keys_list: 字典插入时候需要的顺序key。
        :return:
        """
        if len(dict_array) < 1:
            # return False, "数据不足插入"
            return 0

        _sql_str_list = []
        for _item in dict_array:
            _sql_str = "(\'" + "\',\'".join( [ str(_item[key]).replace("'", "\\dou") for key in keys_list] ) + "\')"
            _sql_str_list.append(_sql_str)

        _query_sql = """insert into {table_name}({columns}) values {values_str};""".format(
            values_str=", ".join([str(x) for x in _sql_str_list]),
            table_name=self.table_name,
            columns=columns_order
        )

        try:
            from  xsqlmb.src.ltool.sqlconn import sql_action
            sql_action(_query_sql)
            return len(_sql_str_list)

        except:
            # 一般来说到不了下面这一步。
            try:
                from  xsqlmb.src.cfgs.logConfig import logging
            except:
                import logging
            logging.info("导入数据库失败！")

            return 0
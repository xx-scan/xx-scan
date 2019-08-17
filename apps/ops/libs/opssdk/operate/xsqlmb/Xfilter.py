class XFilter():

    def __init__(self, filter_column, filter_type, extra):
        """

        :param filter_column: 对象的列
        :param filter_type: 对象的管理类型， 包含，在某某之间，regexp, 排序，
        :param extra: 管理策略
        """
        # self.filters = filters
        self.filter_column=filter_column
        self.filter_type=filter_type
        self.extra=extra

    def response(self):
        """
        多合一
        :return:
        """

        # if self.filter_type == "contains":
        #     return self._contains(_sets=self.extra, _boundary=
        #     self.extra["_boundary"] if "_boundary" in self.extra.keys() else True)

        if self.filter_type == "get":
            return self._get(order_value=str(self.extra))

        if self.filter_type == "contains":
            return self._contains(_sets=self.extra)

        if self.filter_type == "regexp":
            return self._regexp(partern=self.extra)

        if self.filter_type == "between":
            return self._between(_start=self.extra[0], _end=self.extra[1])

        # if self.filter_type == "orderby":
        #     return self._orderd(desc=self.extra if self.extra else True)

        # if self.filter_type == "limit":
        #     return self._limit(self.extra[0], self.extra[1])

        return None

    def _contains(self, _sets, _boundary=True):
        """
        包含的内容集合的相关验证。
        :param _sets: 集合验证
        :param _boundary: 边界就是用不用字符串包裹。一般如果是int就不用, 默认都包含
        :return: 一段sql字符串
        """
        _hock_flag = "\'" if _boundary else ""
        return " {column} in ({column_sets}) ".format(column=self.filter_column,
            column_sets=",".join( [_hock_flag + x + _hock_flag for x in _sets]))

    def _get(self, order_value):
        """
        类似于 where id=22 这种。
        :param order_value:
        :return:
        """
        return " {column}='{order_value}' ".format(column=self.filter_column, order_value=order_value)


    def _regexp(self, partern):
        """
        字符串正则匹配返回过滤。
        :param partern:
        :return:
        """
        return " {column} regexp '{partern}' ".format(column=self.filter_column, partern=partern)

    def _between(self, _start, _end):
        """
        介于两个值之间。
        :param _start:
        :param _end:
        :return:
        """
        if not _start and not _end:
            return ""
        _str1 = " {column} >= '{_start}' ".format(column=self.filter_column, _start=_start) if _start else ""
        _str2 = " {column} <= '{_end}' ".format(column=self.filter_column, _end=_end) if _end else ""
        _and = " and " if _start and _end else ""
        return _str1 + _and + _str2

    @staticmethod
    def _orderd(filter_column, desc=True):
        """
        排序规则是升序还是降序
        :param desc:
        :return:
        """
        return " order by {column} {descd}".format(column=filter_column, descd= "desc" if desc else "")

    @staticmethod
    def _limit(_s, _e):
        """
        限制多少条
        :param _s: 开始的限制值
        :param _e: 结束的限制值
        :return:
        """
        return " limit {limits} ".format(limits=str(_s) if not _e or _e < _s else str(_s) + "," + str(_e))


class WrapperFilter():

    def __init__(self, table_name, filters, columns_show=None):
        """
        返回filter管理的表格的整段sql
        :param table_name:
        :param filters:
        :param columns_show:
        """
        self.filters = filters
        self.columns_show = columns_show
        self.table_name=table_name

    @staticmethod
    def get_self_by_json(json):
        pass

    @staticmethod
    def get_self_demo_json():
        return dict(
            table_name="accesslog",
            columns_show=["device", "server_port", "remote_addr", "user_agent",
                          "body_bytes_sent", "status"],
            filters=[
                {"column": "time_local", "type": "between", "extra": ["2019-3-15", "2019-4-1"]},
                {"column": "server_port", "type": "get", "extra": "8080"},
                {"column": "status", "type": "between", "extra": [None, 300]},
                {"column": 'user_agent', "type": "regexp", "extra": "rome"},
                {"column": 'remote_addr', "type": "contains", "extra": ["192.168.2.160", "127.0.0.1"]},
                {"type": "limit", "extra": [22, 55]}
            ]
        )

    def _wrapped_filters(self, condition_flag="where"):
        l_filters = []
        for filter in self.filters:
            if "type" not in filter.keys():
                return False, "filter 格式错误"
            # if filter["type"] not in filter_types:
            #     return False, "Not Suport This Type"
            _type = filter["type"]
            try:
                resp = XFilter(filter_column=filter["column"], filter_type=filter["type"],
                               extra=filter["extra"]).response()
                if resp:
                    l_filters.append(resp)
            except:
                # 应该是缺少column
                pass

        s_filters = condition_flag + " " + " and ".join(l_filters) if len(l_filters) > 0 else ""

        if "orderby" in [x["type"] for x in self.filters]:
            filter = [x for x in self.filters if x["type"] == "orderby"][0]
            _orderby_filter = XFilter._orderd(filter_column=filter["column"], desc=filter["extra"])
            s_filters += _orderby_filter

        if "limit" in [x["type"] for x in self.filters]:
            filter = [x for x in self.filters if x["type"] == "limit"][0]
            _limit_filter = XFilter._limit(filter["extra"][0], filter["extra"][1])
            s_filters += _limit_filter

        return s_filters

    def _wraped_sqlstr(self):
        _sqls = """select {columns_show} from {table_name} {s_filters} ;""".format(
            columns_show= ",".join(self.columns_show) if self.columns_show else "*",
            table_name=self.table_name,
            s_filters=self._wrapped_filters()
        )
        return _sqls

    @staticmethod
    def test_wrapped():
        _sqlstr = WrapperFilter(**WrapperFilter.get_self_demo_json())._wraped_sqlstr()

        try:
            from xsqlmb.src.ltool.sqlconn import from_sql_get_data
            _sqldata = from_sql_get_data(_sqlstr)["data"]
            for x in _sqldata:
                print(x)
            print(_sqlstr)
        except:
            print(_sqlstr)


class GroupbyFilter():
    def __init__(self, table_obj, groupbyfilters=None, conditions=None):
        """
        {
            "remote_addr": "count",
            "status": None,
        }
        :param gbfilters: group by 的选项
        """
        self.groupbyfilters = groupbyfilters
        self.conditions = conditions
        self.table_obj = table_obj


    def groupy(self):
        _dict = self.groupbyfilters
        l_columns = []
        groupby_keys = ",".join(_dict.keys())
        for column in self.groupbyfilters.keys():
            l_columns.append(column +"," + _dict[column] +"(" + column +") as " + _dict[column]+"_"+column if _dict[column] else column)

        s_columns = ",".join(l_columns)
        s_condtions = WrapperFilter(table_name="localtest",
                filters=self.conditions)._wrapped_filters(condition_flag="having")

        _sql = """select {s_columns} from {table_obj} group by {groupby_keys} {condition} """.format(
            s_columns=s_columns,table_obj=self.table_obj, groupby_keys=groupby_keys,
            condition = s_condtions
        )

        return _sql

    def get_sqldata(self):
        _sqlstr = self.groupy()
        try:
            from xsqlmb.src.ltool.sqlconn import from_sql_get_data
            _sqldata = from_sql_get_data(_sqlstr)["data"]
            for x in _sqldata:
                print(x)
            print(_sqlstr)
        except:
            print(_sqlstr)

    @staticmethod
    def get_json_demo():
        return dict(
            table_obj="accesslog",
            groupbyfilters={"remote_addr": "count", "status": None},
            conditions=[
                dict(column="status", type="between", extra=[400, 500]),
                       dict(column="count_remote_addr", type="orderby", extra=True),
                       dict(type="limit", extra=[10, None]),
                       ]
        )

    @staticmethod
    def get_demo_sqldata():
        GroupbyFilter(**GroupbyFilter.get_json_demo()).get_sqldata()






















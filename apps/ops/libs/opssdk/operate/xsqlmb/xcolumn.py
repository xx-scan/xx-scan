class SqlModeColumnClass():

    def __init__(self, _type, _limit, _default, _column_name, _null=False, _boundary=True):
        """

        :param _type: 类型 Int/char
        :param _limit:  限制多少长度
        :param _default:  默认是多少
        :param _column_name: 列的名字
        :param _null: 默认是否可以插入空类型
        :param _boundary: 限制是用字符韩式原本输出  datetime的TimeStamp 和 int 没有边界
        """
        self._type = _type
        self._limit = _limit
        self._default = _default
        self._column_name = _column_name
        self._null = _null
        self._boundary = _boundary

    def _json(self):
        return dict(_type=self._type, _limit=self._limit, _default=self._default)

    @staticmethod
    def get_verchar255(_column_name):
        return SqlModeColumnClass(_type="varchar", _limit=255, _default="zx_orm_default_str", _column_name=_column_name)

    @staticmethod
    def get_datetime(_column_name):
        return SqlModeColumnClass(_type="datetime", _limit=None, _default='CURRENT_TIMESTAMP', _column_name=_column_name, _boundary=False)

    @staticmethod
    def get_int11(_column_name):
        return SqlModeColumnClass(_type="int", _limit=11, _default=28256, _column_name=_column_name, _boundary=False)

    def get_create_str(self):
        column_name =self._column_name
        column_type = self._type + "({len})".format(len=self._limit) if self._limit else self._type

        column_default = "DEFAULT " + str(self._default) if self._default else ""
        if self._boundary:
            column_default = "DEFAULT \'" + str(self._default) + "\'" if self._default else ""

        return  """`{column_name}` {column_type} {null} {column_default},""".format(
            column_name=column_name,
            column_type=column_type,
            column_default=column_default,
            null="NOT NULL" if not self._null else ""
        )
    @staticmethod
    def get_self_by_dict(json):
        if not any(x in json.keys() for x in ["_type", "_limit", "_default", "_column_name"]):
            return False, "缺少参数"

        return SqlModeColumnClass(
            _type=json["_type"],
            _limit=json["_limit"],
            _default=json["_default"],
            _column_name=json["_column_name"],
            _null=json["_null"] if "_null" in json.keys() else False,
            _boundary=json["_boundary"] if "_boundary" in json.keys() else True,
        )


"""
--修改CreateTime 设置默认时间 CURRENT_TIMESTAMP 
ALTER TABLE `table_name`
MODIFY COLUMN  `CreateTime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' ;

 
--添加UpdateTime 设置 默认时间 CURRENT_TIMESTAMP   设置更新时间为 ON UPDATE CURRENT_TIMESTAMP 
ALTER TABLE `table_name`
ADD COLUMN `UpdateTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' ;

"""
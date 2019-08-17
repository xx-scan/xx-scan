"""
数据库操作的核心管理类

包含但不限于 create / update / alter / delete
"""

class SqlTableOpreationClass():
    def __init__(self, table_name):
        self.table_name = table_name


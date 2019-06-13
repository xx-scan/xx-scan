import pymysql

from xsqlmb.src.cfgs.basicConfig import MPP_CONFIG



def from_sql_get_data(sql):
    # Connect to the database
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    try:
        res = corsor.fetchall()
        try:
            data = {"data": res, "heads": [x[0] for x in corsor.description]}
        except:
            data = None
            try:
                from xsqlmb.src.cfgs.logConfig import logging
            except:
                import logging
            logging.error({"query_sql": sql, "stat": 0})
    finally:
        ## connection.commit()
        corsor.close()
        connection.close()
    return data


## 单纯执行的
def sql_action(sql):
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()

    try:
        corsor.execute(sql)
        connection.commit()
    # print(sql)
    except :
        try:
            from xsqlmb.src.cfgs.logConfig import logging
        except:
            import logging
        logging.error({"query_sql": sql, "stat": 0})
    finally:
        corsor.close()
        connection.close()
    return True
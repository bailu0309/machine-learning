# -*- coding: utf-8 -*-
# @Time : 2020/3/28 : 10:36
# @Author: bailu
import cx_Oracle


def loadData():
    con = cx_Oracle.connect('')
    db_cursor = con.cursor()
    sql_cmd = "select * from table t "
    db_cursor.execute(sql_cmd)
    postingList = []
    label = []
    for row in db_cursor:
        v = row[-1]
        label.append(v)
        postingList.append(row[:10])

    db_cursor.close()
    con.close()
    return postingList, label


print loadData()

# -*- coding: utf-8 -*-
# @Time : 2020/3/28 : 10:36
# @Author: bailu
import cx_Oracle


def loadData():
    con = cx_Oracle.connect('mrqc_wt/mrqc_wt@192.168.1.22/dev33')
    db_cursor = con.cursor()
    sql_cmd = "select xb,nl,zy,hy,jbdm,jbdm2,jbdm3,ssjczbm1,ssjczbm2,ssjczbm3,LABEL from T_WT_TEST t "
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


def loadTestData():
    con = cx_Oracle.connect('mrqc_wt/mrqc_wt@192.168.1.22/dev33')
    db_cursor = con.cursor()
    sql_cmd = "select xb,nl,zy,hy,jbdm,jbdm2,jbdm3,ssjczbm1,ssjczbm2,ssjczbm3 from T_WT_TEST t where xb = '1' "
    db_cursor.execute(sql_cmd)
    postingList = []

    for row in db_cursor:
        postingList.append(row)

    db_cursor.close()
    con.close()
    return postingList


print loadTestData()

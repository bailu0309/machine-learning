# -*- coding: utf-8 -*-
# @Time : 2020/4/16 : 17:40
# @Author: bailu

import configparser as configparser
from numpy import *
import cx_Oracle
import ConfigParser
import os
import logRegres as lr


def getConfig(k):
    cfg = "./config.cfg"
    config_raw = ConfigParser.RawConfigParser()
    config_raw.read(cfg)
    # 读取配置文件中 [DEFAULT]
    database = config_raw.defaults()
    # 读取指定section下的value值
    url = config_raw.get('DATABASE', k)
    return url


def loadTrainData():
    con = cx_Oracle.connect(getConfig('urldir'))
    db_cursor = con.cursor()
    sql_cmd = "select xb,hy,jbdm,jbdm2,jbdm3,ssjczbm1,ssjczbm2,ssjczbm3,LABEL from T_WT_TEST t "
    db_cursor.execute(sql_cmd)
    postingList = []
    label = []
    for row in db_cursor:
        v = row[-1]
        label.append(v)
        postingList.append(row[:8])

    db_cursor.close()
    con.close()
    return postingList, label


def loadTestData(num):
    con = cx_Oracle.connect(getConfig('urldir'))
    db_cursor = con.cursor()
    sql_cmd = "select * from  (select xb,zy,hy," \
              "decode(t.jbdm, null, '0', substr(jbdm, 0, 3)) jbdm," \
              "decode(t.jbdm2, null, '0', substr(jbdm2, 0, 3)) jbdm2," \
              "decode(t.jbdm3, null, '0', substr(jbdm3, 0, 3)) jbdm3," \
              "decode(t.ssjczbm1, null, '0', substr(ssjczbm1, 0, 2)) ssjczbm1," \
              "decode(t.ssjczbm2, null, '0', substr(ssjczbm2, 0, 2)) ssjczbm2," \
              "decode(t.ssjczbm3, null, '0', substr(ssjczbm3, 0, 2)) ssjczbm3 " \
              "    from wt_base t " \
              "         where zfy > 10000 " \
              "               and not exists (select 1 from t_wt_test t1 where t.bah = t1.bah) order by dbms_random.value ) " \
              "      where rownum <= " + str(num)
    db_cursor.execute(sql_cmd)
    postingList = []

    for row in db_cursor:
        postingList.append(row)

    db_cursor.close()
    con.close()
    return postingList


def loadTestData2(num):
    con = cx_Oracle.connect(getConfig('urldir'))
    db_cursor = con.cursor()
    sql_cmd = "select * from  (select xb,hy," \
              "decode(t.jbdm, null, '0', substr(jbdm, 0, 3)) jbdm," \
              "decode(t.jbdm2, null, '0', substr(jbdm2, 0, 3)) jbdm2," \
              "decode(t.jbdm3, null, '0', substr(jbdm3, 0, 3)) jbdm3," \
              "decode(t.ssjczbm1, null, '0', substr(ssjczbm1, 0, 2)) ssjczbm1," \
              "decode(t.ssjczbm2, null, '0', substr(ssjczbm2, 0, 2)) ssjczbm2," \
              "decode(t.ssjczbm3, null, '0', substr(ssjczbm3, 0, 2)) ssjczbm3 " \
              "    from wt_base t " \
              "         where zfy < 10000 " \
              "               and not exists (select 1 from t_wt_test t1 where t.bah = t1.bah) order by dbms_random.value ) " \
              "      where rownum <= " + str(num)
    db_cursor.execute(sql_cmd)
    postingList = []

    for row in db_cursor:
        postingList.append(row)

    db_cursor.close()
    con.close()
    return postingList


def costTest(intNum=100):
    trainingSet, traingLabels = loadTrainData()
    # trainingSet = []
    # traingLabels = []
    # for line in frTrain.readlines():
    #     currLine = line.strip().split('\t')
    #     lineArr = []
    #     for i in range(21):
    #         lineArr.append(float(currLine[i]))
    #     trainingSet.append(lineArr)
    #     traingLabels.append(float(currLine[21]))
    trainWeights = lr.stocGradAscent1(array(trainingSet), traingLabels, intNum)
    # print "trainWeights: %f" % trainWeights

    errorCount = 0
    numTestVec = 0.0

    frTest = open('horseColicTest.txt')

    # 需要对非数值型数据进行处理

    # testData = loadTestData()
    #
    # for line in testData:
    #     numTestVec += 1.0
    #     lineArr = []
    #     for i in range(21):
    #         lineArr.append(float(currLine[i]))
    #     if int(lr.classifyVector(array(lineArr), trainWeights)) != int(currLine[21]):
    #         errorCount += 1
    # errorRate = float(errorCount) / numTestVec
    # print "错误率：%f" % errorRate
    # return errorRate

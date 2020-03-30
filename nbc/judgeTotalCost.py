# -*- coding: utf-8 -*-
# @Time : 2020/3/23 : 11:34
# @Author: bailu
# 判断患者总费用是否大于1W

# 初始数据
import configparser as configparser
from numpy import *
import cx_Oracle
import ConfigParser
import os


def getConfig(k):
    cfg = "./config.cfg"
    config_raw = ConfigParser.RawConfigParser()
    config_raw.read(cfg)
    # 读取配置文件中 [DEFAULT]
    database = config_raw.defaults()
    # 读取指定section下的value值
    url = config_raw.get('DATABASE', k)
    return url


def loadData2():
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


# 去重
def createVocabList(dataSet):
    """
    创建词汇列表
    :param dataSet:数据集
    :return:词汇列表
    """
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)

    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    """
    创建词汇向量
    :param vocabList: 词汇表
    :param inputSet:数据集
    :return:词汇向量
    """
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word:%s is not in " % word
    return returnVec


def trainNB0(trainMatrix, trainCategory):
    """

    :param trainMatrix:  文档矩阵
    :param trainCategory: 类别向量
    :return:
    """
    numTrainDocs = len(trainMatrix)  # 文档个数
    numWords = len(trainMatrix[0])  # 第一个文档的单词数
    pAbusive = sum(trainCategory) / float(numTrainDocs)  # 坏发言的概率

    p0Num = ones(numWords)
    p1Num = ones(numWords)

    p0Denom = 2.0  # 0.0
    p1Denom = 2.0  # 0.0

    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    p1Vect = log(p1Num / p1Denom)
    p0Vect = log(p0Num / p0Denom)

    return p0Vect, p1Vect, pAbusive


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)

    if p1 > p0:
        return 1
    else:
        return 0


def testingNB():
    listOPosts, listClasses = loadData2()
    myVocabList = createVocabList(listOPosts)
    trainMat = []

    num = 5

    for postingDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postingDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = loadTestData(num)
    print '-------1---------'
    i = 0
    for v in testEntry:
        thisDoc = array(setOfWords2Vec(myVocabList, v))
        cf = classifyNB(thisDoc, p0V, p1V, pAb)
        i += cf
        print v, '类别：', cf

    print '-------2---------'
    testEntry = loadTestData2(num)
    j = 0
    for v in testEntry:
        thisDoc = array(setOfWords2Vec(myVocabList, v))
        cf = classifyNB(thisDoc, p0V, p1V, pAb)
        if cf == 0:
            j += 1
        print v, '类别：', cf

    print '正确率：', float(i + j) * 100 / (num * 2), '%'


testingNB()

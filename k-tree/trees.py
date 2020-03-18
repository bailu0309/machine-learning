# -*- coding: utf-8 -*-
from math import log
import operator


# 获取香农熵值
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
            labelCounts[currentLabel] += 1

    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)

    return shannonEnt


# 创建数据集
def createDataSet():
    dataSet = [[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


# 按特征值分割数据
def spliteDataSet(dataSet, axis, value):
    """ 按特征值分割数据
    :param dataSet: 数据
    :param axis: 特征值位置
    :param value: 特征值
    :return: 掉特征值的数组
    """
    retDataSet = []
    for featVet in dataSet:
        if (featVet[axis] == value):
            # 返回去掉特征值的数组
            reducedFeatVec = featVet[:axis]
            reducedFeatVec.extend(featVet[axis + 1:])
            retDataSet.append(reducedFeatVec)

    return retDataSet


# 选择最好的特征分组
def chooseBestFeatureToSplit(dataSet):
    """
    选择最好的特征分组
    :param dataSet:
    :return: 最好的特征值的位置
    """
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1

    for i in range(numFeatures):
        # 将dataSet中的数据先按行依次放入example中，然后取得example中的example[i]元素，放入列表featList中
        featList = [example[i] for example in dataSet]
        # 去重特征值
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = spliteDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)

        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


myDate, myLabel = createDataSet()

shang = calcShannonEnt(myDate)
print shang

print spliteDataSet(myDate, 2, 'yes')
print chooseBestFeatureToSplit(myDate)

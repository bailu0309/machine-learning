# -*- coding: utf-8 -*-
# @Time : 2020/3/30 : 16:25
# @Author: bailu

from numpy import *


def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


def sigmoid(inX):
    """
    Sigmoid函数
    :param inX: 实数
    :return: 0-1
    """
    if inX >= 0:  # 对sigmoid函数的优化，避免了出现极大的数据溢出
        return 1.0 / (1 + exp(-inX))
    else:
        return exp(inX) / (1 + exp(inX))


def gradAscent(dataMatIn, classLabels):
    """
    梯度上升算法
    :param dataMatIn: 2维numpy数组 列代表特征 行代表样本
    :param classLabels: 类别标签 1*100的行向量
    :return: 回归系数
    """
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    m, n = shape(dataMatrix)
    alpha = 0.001  # 步长
    maxCycles = 500  # 迭代次数
    weights = ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)  # 列向量
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose() * error

    return weights


def stocGradAscent0(dataMatrix, classLabels):
    m, n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights


def stocGradAscent1(dataMatrix, classLabels, numInt=150):
    """
    随机梯度上升算法
    :param dataMatrix:  数据集
    :param classLabels:  类别
    :param numInt: 迭代次数
    :return:
    """
    m, n = shape(dataMatrix)  # 获取矩阵的维数 m行n列
    weights = ones(n)  # 创建n列参数为1的一维数组
    for j in range(numInt):  # 循环设定的次数
        dataIndex = range(m)  # 创建长度为m的整数列表
        for i in range(m):  # 遍历m次
            alpha = 4 / (1.0 + j + i) + 0.0001  # 每次调整
            randIndex = int(random.uniform(0, len(dataIndex)))  # 随机选取样本更新回归系数
            theChosenOne = dataIndex[randIndex]  # 修复原作者随机选择时，可能重复选择同一数据的问题
            h = sigmoid(sum(dataMatrix[theChosenOne] * weights))
            error = classLabels[theChosenOne] - h
            weights = weights + alpha * error * dataMatrix[theChosenOne]
            del [dataIndex[randIndex]]
    return weights


def plotBestFit(weights):
    """
    画出决策边界
    :param weights:
    """
    import matplotlib.pyplot as plt
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


def classifyVector(intX, weights):
    """
    根据特征向量和回归系数获取sigmoid值，根据sigmoid返回类别
    :param intX: 特征值
    :param weights: 回归系数
    :return: 0 或 1
    """
    prob = sigmoid(sum(intX * weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0


def colicTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainingSet = []
    traingLabels = []
    for line in frTrain.readline():
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        traingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet), traingLabels, 1000)

    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readline():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights)) != int(currLine[21]):
            errorCount += 1
    errorRate = float(errorCount) / numTestVec
    print "错误率：%f" % errorRate
    return errorRate


# def test():
#     dataMat, labelMat = loadDataSet()
#     # weights = gradAscent(dataMat, labelMat)
#     # plotBestFit(weights.getA())
#
#     # weights = stocGradAscent0(array(dataMat), labelMat)
#     weights = stocGradAscent1(array(dataMat), labelMat)
#     plotBestFit(weights)


def colicTest(intNum=100):
    frTrain = open('horseColicTraining.txt');
    frTest = open('horseColicTest.txt')
    trainingSet = []
    traingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        traingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet), traingLabels, intNum)
    # print "trainWeights: %f" % trainWeights

    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights)) != int(currLine[21]):
            errorCount += 1
    errorRate = float(errorCount) / numTestVec
    print "错误率：%f" % errorRate
    return errorRate


for i in range(10):
    colicTest(i * 100)

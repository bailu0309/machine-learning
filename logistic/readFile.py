# -*- coding: utf-8 -*-
# @Time : 2020/4/16 : 14:26
# @Author: bailu


def readFile():
    frTrain = open('horseColicTraining.txt');
    frTest = open('horseColicTest.txt')
    for line in frTrain.readlines():
        print line


readFile()
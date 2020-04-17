# -*- coding: utf-8 -*-
# @Time : 2020/3/23 : 15:15
# @Author: bailu

import jieba

data = jieba.cut("你好啊，请问你是谁？")


for item in data:
    print(item)
print(data)

# -*- coding: gbk -*-
# @Time : 2020/3/23 : 13:36
# @Author: bailu
# 导入相关库
import re

import pandas as pd
import jieba

# 读取数据
data = pd.read_csv('a.csv', encoding='gbk')

for n in data['NAME']:
    n = re.sub("[:：]", "", n)  # 去标点符号
    flag = False
    # print '------' + n
    da = jieba.cut(n)
    for v in da:
        if v == '':
            continue
        if flag:
            print v
        if v == '体温'.decode('gbk') or v == '脉搏'.decode('gbk') or v == '呼吸'.decode('gbk') or v == '血压'.decode(
                'gbk') or v == '吸烟'.decode('gbk') or v == '婚姻状况'.decode('gbk'):
            print v
            flag = True
        else:
            flag = False
# 查看数据

#
# for item in data:
#     print(item)
# fc = jieba.cut(item)
# for val in fc:
#     print(val)

print "------------------"

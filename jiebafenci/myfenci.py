# -*- coding: gbk -*-
# @Time : 2020/3/23 : 13:36
# @Author: bailu
# ������ؿ�
import re

import pandas as pd
import jieba

# ��ȡ����
data = pd.read_csv('a.csv', encoding='gbk')

for n in data['NAME']:
    n = re.sub("[:��]", "", n)  # ȥ������
    flag = False
    # print '------' + n
    da = jieba.cut(n)
    for v in da:
        if v == '':
            continue
        if flag:
            print v
        if v == '����'.decode('gbk') or v == '����'.decode('gbk') or v == '����'.decode('gbk') or v == 'Ѫѹ'.decode(
                'gbk') or v == '����'.decode('gbk') or v == '����״��'.decode('gbk'):
            print v
            flag = True
        else:
            flag = False
# �鿴����

#
# for item in data:
#     print(item)
# fc = jieba.cut(item)
# for val in fc:
#     print(val)

print "------------------"

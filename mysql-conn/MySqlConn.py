# -*- coding: utf-8 -*-
# @Time : 2020/3/27 : 13:57
# @Author: bailu

import mysql.connector

mydb = mysql.connector.connect(
    host="192.168.1.16",
    user="NQC",
    passwd="NQC",
    database="NQC"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM m_role")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)

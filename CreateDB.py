# -*- coding: utf-8 -*-
#初始化数据库
import os
import sqlite3

db = os.path.dirname(os.path.realpath(__file__)) + "\\scanner.db"
print(db)
'''
    #新建数据库
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute('create table allbar (barcode char(17) primary key, batchnum char(6),createtime char(21), shift char(16))')
    #cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
    cursor.close()
    connection.commit()
    connection.close()
'''
connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("PRAGMA table_info(allbar)") 
print('各字段')
for x in cursor.fetchall():print(x)
    


cursor.execute('select * from allbar ')
print('所有记录 ：')
for x in cursor.fetchall():print(x)


cursor.close()
connection.commit()
connection.close()



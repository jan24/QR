#coding=utf-8
#创建数据库表
# show columns from barcode 显示各字段信息, show tables 列出各数据表
import mysql.connector
conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)

cursor = conn.cursor()
# 序号 条码 批次 扫码时间 班次2017-11-28-5-1 是否是新条码
sql = '''create table barcode (
                id integer primary key auto_increment,
                bar char(18),
                batchnum char(6),
                createtime timestamp default current_timestamp,
                shift char(16),
                isnew boolean default True  )'''

cursor.execute(sql)
conn.commit()


cursor = conn.cursor()
#每批次订单的信息，id, 批次号，工厂型号，颜色，计划量，createtime
sql = '''create table products (
                id integer primary key auto_increment,
                batchnum char(6) not null,
                factory_model char(29),
                color char(3),
                factory_num smallint,
                UNIQUE (batchnum))'''
cursor.execute(sql)
conn.commit()
conn.close()

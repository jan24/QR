#coding=utf-8
#MySQL驱动 mysql-connector-python
#封装读写语句
import mysql.connector
#检查表是否存在
try:
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    cursor.execute('show tables')
    if not 'barcode' in cursor.fetchall()[0]:
        raise ValueError('数据库表barcode不存在')
    conn.close()
except Exception:
    print('无法连接上数据库 ')
print('>>>数据库连接测试正常 ')


#插入一行记录
def insert(bar, shift, isnew=1):
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    sql = 'insert into barcode(bar, batchnum, shift,isnew) values (%s, %s, %s, %s)'
    cursor.execute(sql,[bar, bar[4:10], shift, isnew]) #批次号为条码的部分，368A 7N8198 00127
    conn.commit()
    conn.close()

#查询条码是否已存在
def query_bar_isnew(bar):
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    sql = 'select * from barcode where bar = %s'
    cursor.execute(sql, (bar,))
    values = cursor.fetchall()
    conn.close()
    if len(values) == 0:
        return True
    else:
        return False    

#查询某班次的总采集数量
def shift_count(shift):
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    sql = 'select count(*) from barcode where shift = %s and isnew = 1 '
    cursor.execute(sql, (shift,))
    values = cursor.fetchall()
    conn.close()
    return values[0][0]

#查询某班次的某批次号的总采集数
def batch_count(batchnum, shift):
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    sql = 'select count(distinct bar) from barcode where batchnum = %s and shift = %s'
    cursor.execute(sql, (batchnum, shift))
    values = cursor.fetchall()
    conn.close()   
    return values[0][0]

#查询某批次号的历史总采集数量（即所有班次的）
def batch_allcount(batchnum):
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    sql = 'select count(distinct bar) from barcode where batchnum = %s'
    cursor.execute(sql, (batchnum, ))
    values = cursor.fetchall()
    conn.close()   
    return values[0][0]

def get_maxid_bar():
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    cursor.execute('select max(id) from barcode')   
    values = cursor.fetchall()
    maxid = values[0][0]
    cursor.execute('select * from barcode where id = %s' % (maxid,) )  #注意这种写法传字符串时容易出问题
    values = cursor.fetchall() # 返回的是tuple,例如(96, 'g4234234634686', '423463', datetime.datetime(2018, 4, 19, 22, 4, 52), '2018-04-19-6-2'，1)
    conn.close()
    if not len(values)==0:
        return values[0] 

#查询某班次的采集的所有批次，返回批次号的列表
def batch_list(shift):
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    sql = 'select distinct batchnum from barcode where shift = %s'
    cursor.execute(sql, (shift,))
    values = cursor.fetchall()
    li=[tupl[0] for tupl in values]
    return li

#按批次号查询products表中的订单信息,返回的是tuple
def product_info_tuple(batchnum):
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    sql = 'select * from products where batchnum = %s'
    cursor.execute(sql, (batchnum, ))
    values = cursor.fetchall()
    conn.close()
    if not len(values)==0:
        return values[0]
#coding=utf-8
import db_orm
import mysql.connector
import random
import time


#products 表的信息
def insert(batchnum, factory_model, color, factory_num):
    time.sleep(1)
    conn = mysql.connector.connect(user='root', password='password', database='Qrbarcode', use_unicode=True)
    cursor = conn.cursor()
    sql = 'insert into products(batchnum, factory_model, color, factory_num) values (%s, %s, %s, %s)'
    cursor.execute(sql,(batchnum, factory_model, color, factory_num)) #批次号为条码的部分，368A 7N8198 00127
    conn.commit()
    conn.close()


#DF1-112-CW0K0-AE1L0-HER2

m=['DD1-051-CW2K0','DF1-070-C40J0','DF1-070-CW0K0','DF1-080-C50J0','DF1-080-CW0K0','DF1-090-CW0J0','DF1-090-CW0K0','DF1-112-C50K0','DF1-141-CS2K0','DF2-110-C40J0','DF2-110-C50K0','DF2-110-CW0K0','DL1-050-CW0K0','DL1-060-CW0K0','DL1-070-C50J0','DL1-112-CW0K0','WE1-150-CW0K0','WM1-060-CW0K0','WM1-150-CW0K0']
n=['AE1L0', 'AIN10', 'DF1L1', 'AE100', 'ABKK0', 'AHXL0', 'AD5L0', 'AE1L0', 'AWPL1', 'AE1K1', 'AE1K1', ]
k=['-HER2', '-AV91', '-HM1', '-MCF9', '-MM2', '-WLP', '-CTN1', '-HER1', '-OST', '-BN92', '-ETX2', ]

def a_product(x):
    if 0<= x <=9:
        x='0'+str(x)
    else:
        x=str(x)
    a ='7N00' + x
    b=random.choice(m)+'-'+random.choice(n)+random.choice(k)
    c=random.choice ( ['A02', 'B01', 'C03', 'D10', 'C28','V01','A13'] )
    d=random.choice ( [110, 254, 512, 1440, 4400 , 1052, random.randint(200, 500),random.randint(400, 800),random.randint(1000, 8000)] )
    return(a, b, c, d)

# 7N0000 -7N0099
def main():
    for x in range(0,100):
        pro = a_product(x)
        print(pro)
        insert(*pro)


if __name__ == '__main__':
    main()

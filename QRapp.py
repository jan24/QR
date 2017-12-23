# -*- coding: utf-8 -*-
import os, sys, winsound, time
import re
import sqlite3
from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',**barcode_now)
@app.route('/index')
def _index():
    return redirect('/')
@app.route('/readme')
def readme():
    return render_template('readme.html')
@app.route('/linechart')
def linechart():
    return render_template('linechart.html')




#ORM框架
def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
def get_current_time2():
    return time.strftime('%m-%d %H:%M', time.localtime(time.time()))

def set_shift(date,xian,shift):
    pass    

def get_shift():
    return '2017-12-20-5-0'


class Database:
    db = os.path.dirname(os.path.realpath(__file__)) + "\\scanner.db"
    charset = 'utf8'
    def __init__(self):
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
    def query(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    def insert(self,query,params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except:
            self.connection.rollback()
    def __del__(self):
        self.connection.close()


def query_bar_exist(s):
    #查询条码是否已存在
    my_db = Database()
    query_by_sql = 'select * from allbar where barcode=?'
    query_list = my_db.query(query_by_sql,(s,))
    if len(query_list)==0:
        return False
    else:
        return True

def insert_bar(s):
    #插入新条码
    barcode = s
    batchnum = s[4:10]
    createtime = get_current_time()
    shift = get_shift()    
    query_by_sql = 'insert into allbar (barcode, batchnum, createtime, shift) values(?,?,?,?)'
    try:
        my_db = Database()
        my_db.insert(query_by_sql,(barcode, batchnum, createtime, shift))
    except Exception as e:
        print(e)



soundFile_dict = { 'new':os.path.dirname(os.path.realpath(__file__)) + "\\music\\railway.wav", 
'old':os.path.dirname(os.path.realpath(__file__)) + "\\music\\horse.wav",
 'bad':os.path.dirname(os.path.realpath(__file__)) + "\\music\\wolf.wav" } #只接受WAV文件

def playmusic(status):
    #status must be 'new' 'old' 'bad'
    winsound.PlaySound(soundFile_dict.get(status), winsound.SND_ASYNC)


pattern = r'\d{3}\w\d\w{2}\d{8}$' #校对冷媒码

def scan():
    print(" 正在监听键盘 .......")
    while True:
        s = str(sys.stdin.readline()).strip("\n")
        if re.match(pattern, s):
            if query_bar_exist(s):
                status='old'
                print('plyamusic old')
            else:
                insert_bar(s)
                status='new'
                print('plyamusic new')
        else:
            status='bad'
            print('plyamusic bad')
        playmusic(status)

barcode_now = { 'barcode':'456A7N009800027',
                'status':'new',
                'batchnum':'7N0098',
                'fac_model':'DF1-112-CW0K0-AE1L0-HER2',
                'color':"B01",
                'time_now':"12-22 23:09",
                'total':3040 
               }




if __name__=="__main__":
    
    app.run()
    scan()




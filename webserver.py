#coding=utf-8
from flask import Flask
from flask import render_template, redirect
import db_orm
import time, datetime

app = Flask(__name__)
@app.route('/readme') #静态页面
def readme():
    return render_template('readme.html')

@app.route('/linechart')
def linechart():
    return render_template('linechart.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    current_bar()
    barcode_now = { 
                'date': get_current_time1(),
                'line':'总 %s 车间' % C_Bar.shift[11],
                'shift':{'1':'白班','2':'晚班','3':'中班'}[C_Bar.shift[-1]],
                'bar':C_Bar.bar,
                'status':{0:'旧条码',1:'新条码'}[C_Bar.isnew],
                'batchnum':C_Bar.batchnum,
                'fac_model':'DF1-112-CW0K0-AE1L0-HER2',
                'color':"B01",
                'time_now':get_current_time2(),
                'total':C_Bar.Shcount
               }
    return render_template('index.html',**barcode_now)

class C_Bar:
    #保存当前条码的各个状态
    pass

def current_bar():
    #查询当前条码的扫码信息
    q1 = db_orm.get_maxid_bar()
    if q1 is None:
        pass
    else:
        C_Bar.bar = q1[1]
        C_Bar.batchnum = q1[2]
        C_Bar.tstamp = q1[3]
        C_Bar.shift = q1[4]
        C_Bar.isnew = q1[5]
        C_Bar.count = db_orm.batch_count(C_Bar.batchnum, C_Bar.shift)
        C_Bar.allcount = db_orm.shift_count(C_Bar.batchnum)
        C_Bar.Shcount = db_orm.shift_count(C_Bar.shift)
    #查询当前条码的所属批次的产品信息
'''
    C_Bar.factory_model
    C_Bar.color
    C_Bar.factory_num

    C_Bar.count = C_Bar.factory_num - C_Bar.allcount
    '''

def get_current_time1():
    return time.strftime('%m-%d', time.localtime(time.time()))
def get_current_time2():
    return time.strftime('%m-%d %H:%M', time.localtime(time.time()))
#批次的信息用不着每次都查数据库，故建立个当前所有批次的字典
#batch_list = 




if __name__ == '__main__':
    app.run()
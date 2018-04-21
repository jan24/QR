#coding=utf-8
from flask import Flask, render_template, redirect
from flask_script import Manager
import db_orm
import time, datetime


app = Flask(__name__)



#manager = Manager(app)


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
    #查询最新的条码，以之班次为当前的班次
    current_bar() 
    #查询当前班次有扫码的所有批次
    li = db_orm.batch_list(C_Bar.shift)
    raw_count = min(len(li), 30) #设置最多显示30个
    #获取当前班次所有批次的历史完成数和当班采集数，返回字典
    count_dict = {}
    for batch in li:
        count_dict[batch] = (db_orm.batch_allcount(batch),)+(db_orm.batch_count(batch, C_Bar.shift),)

    alldict = { 'date': get_current_time1(),
                'line':'总 %s 车间' % C_Bar.shift[11],
                'shift':{'1':'白班','2':'晚班','3':'中班'}[C_Bar.shift[-1]],
                'bar':C_Bar.bar,
                'status':{0:'旧条码',1:'新条码'}[C_Bar.isnew],
                'batchnum':C_Bar.batchnum, #批次号
                'fac_model':pdict.get(C_Bar.batchnum)[2],#'DF1-112-CW0K0-AE1L0-HER2' # pdict是全局变量
                'color':pdict.get(C_Bar.batchnum)[3],  #"B01"
                'time_now':get_current_time2(),
                'total':C_Bar.Shcount, #当班总采集量
                'pdict':pdict, # index模板中的表格数据，产品信息
                'count_dict':count_dict, #index模板中的表格数据，产量
                'raw_count':raw_count, # 表格的行数
                'li':li,                
               }
    return render_template('index.html', **alldict)

class C_Bar:
    #保存当前条码的各个状态
    pass

def current_bar():
    #查询当前条码的扫码信息
    q1 = db_orm.get_maxid_bar()
    if q1:
        C_Bar.bar = q1[1]
        C_Bar.batchnum = q1[2]
        C_Bar.tstamp = q1[3]
        C_Bar.shift = q1[4]
        C_Bar.isnew = q1[5]
        C_Bar.count = db_orm.batch_count(C_Bar.batchnum, C_Bar.shift)
        C_Bar.allcount = db_orm.shift_count(C_Bar.batchnum)
        C_Bar.Shcount = db_orm.shift_count(C_Bar.shift)

def get_current_time1():
    return time.strftime('%m-%d', time.localtime(time.time()))
def get_current_time2():
    return time.strftime('%m-%d %H:%M', time.localtime(time.time()))

class product_dict(dict):
    def __init__(self, **kw):
        super().__init__(self, **kw)
    #会逐步保存当前所有批次的订单信息，{'batchnum':(id, batchnum, factory_model, color, factory_num)}
    #批次为类的key,value值返回tuple
    #当查询到新批次时
    def get(self, key):
        if not key in self.keys():
            self[key] = db_orm.product_info_tuple(key)
            return db_orm.product_info_tuple(key)
        else:
            return self[key]



pdict = product_dict() #也可以放在index()里面， 作为全局变量时可减少对products表的访问次数




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

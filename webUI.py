# -*- coding: utf-8 -*-
#flask
from flask import Flask, render_template, redirect
from flask_socketio import SocketIO

import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


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


barcode_now = {	'barcode':'456A7N009800027',
				'status':'new',
				'batchnum':'7N0098',
				'fac_model':'DF1-112-CW0K0-AE1L0-HER2',
				'color':"B01",
				'time_now':'12-23 15:28',
				'total':3064
			   }



if __name__=="__main__":
	socketio.run(app)



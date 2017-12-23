# -*- coding: utf-8 -*-
#flask
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

barcode_now = {	'barcode':'456A7N009800027',
				'status':'new',
				'batchnum':'7N0098',
				'fac_model':'DF1-112-CW0K0-AE1L0-HER2',
				'color':"B01",
				'time_now':"12-22 23:09",
				'total':3040 
			   }



if __name__=="__main__":
	app.run()

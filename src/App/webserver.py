#!/usr/bin/env python
from flask import Flask, render_template,request, redirect, url_for
import os

app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def hello():
	templateData = {
	'title' : 'LiDAR!',
	}
	if request.method == 'POST':
		if request.form['calibrar']=='Calibrar':
			os.system("python calibrar.py")
			# gpio.output(18, gpio.HIGH)
	return render_template('main.html', **templateData)
@app.route("/scan", methods=["GET","POST"])
def Scan():
	scan= {
	'title': 'Escanear',
	}
	if request.method=='POST':
		name=request.form['name']
		inf=request.form['inf']
		sup=request.form['sup']
		pitch=request.form['pitch']
		yaw=request.form['yaw']
		email=request.form['email']
		os.system("python scan.py"+" "+name+" "+inf+" "+sup+" "+pitch+" "+yaw+" "+email)
		next=request.args.get('next',None)
		if next:
			return redirect(next)
		return redirect(url_for('hello'))
	return render_template('scan.html',**scan)
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8080, debug=True)


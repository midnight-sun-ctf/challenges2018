#! usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, send_from_directory

import uuid
import time
import config
import os
import socket
import urlparse
import urllib2
import re
import opengraph
import requests
from wand.image import Image

# Initialization of variables and modules
app = Flask(__name__)
app.config.from_object('config')

def get_remote_address():
	return request.remote_addr

## ROUTES

@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('img', path)

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html", page="how_to")

@app.route('/')
@app.route('/pagerankr', methods=['GET', 'POST'])
def pagerankr():
	if request.method == 'GET':
		return render_template('pagerankr.html', page='pagerankr')
	else:
		if request.form.get('link') == None:
			return render_template('pagerankr.html', page='pagerankr', error="Invalid request!")
		if not re.match("^https?://[^/]+/.*$", request.form.get('link')):
			return render_template('pagerankr.html', page='pagerankr', error="Invalid link!")
		link = request.form.get('link')
		try:
			res = requests.get(link, allow_redirects=False, timeout=2)
		except Exception as e:
			print e
			return render_template('pagerankr.html', page='pagerankr', error="Page could not be retrieved!")

		og = opengraph.OpenGraph()
		try:
			og.parser(res.content)
		except:
			return render_template('pagerankr.html', page='pagerankr', error="Page could not be parsed!")
			pass
		if not 'site_name' in og:
			og['site_name'] = link
		if 'image' in og:
			if re.match("^https?://[^/]+/.*$", og['image']):
				try:
					imgres = requests.get(og['image'], allow_redirects=False, timeout=2)
					filename = 'img/'+str(uuid.uuid4().hex)
					with open(filename, 'w') as f:
						f.write(imgres.content)
					try:
						print "Trying without MVG"
						with Image(filename=filename) as img:
							with img.clone() as i:
								i.resize(50, 50)
								i.save(filename=filename+".png")
					except:
						print "Trying MVG"
						with Image(filename="mvg:"+filename) as img:
							with img.clone() as i:
								i.resize(50, 50)
								i.save(filename=filename+".png")
					os.remove(filename)
					og['image'] = '/'+filename+".png"
				except Exception as e:
					print e
					try:
						os.remove(filename)
					except:
						pass
					del og['image']
					pass
		og['score'] = (len(og.keys()) * 0.2) + (len(link.split("/")[2]) * 0.12) + (len(res.content) / 15) * 0.11
		return render_template("pagerankr.html", page="pagerankr", og=og)

@app.after_request
def after_request(response):
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('Server', 'nginx')
    return response

## RUN APP
if __name__ == "__main__":
	app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG, threaded=True)

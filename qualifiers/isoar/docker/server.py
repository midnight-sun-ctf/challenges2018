#!/usr/bin/env python3

from gevent.wsgi import WSGIServer
from flask import Flask, jsonify
from util import AlphanumConverter, verify_hash, calculate_hints, calculate_score

wordlist = list(set([x.strip() for x in open("static/public.password.list").readlines()]))
adminpassword = open("adminpass").read().strip()
wordlist += [adminpassword]
flag = open("flag").read().strip()

app = Flask(__name__)
app.url_map.converters['alphanum'] = AlphanumConverter

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/robots.txt')
def robotstxt():
    return app.send_static_file('robots.txt')

@app.route('/pwmeter/<alphanum:password>/<alphanum:proof>')
@verify_hash(prefix="1337")
def pwmeter(password, proof, h=None):
    hints = calculate_hints(wordlist, password)
    score = calculate_score(password)

    if h != None and len(hints) > 0:
        lastbyte = h[-2:]
        hintindex = int(lastbyte, 16) % len(hints)
        hint = hints[hintindex]
    else:
        hint = "; ".join(hints)

    return jsonify(analysis=hint, score=score)

@app.route('/login/<alphanum:password>/<alphanum:proof>')
@verify_hash(suffix="66666")
def login(password, proof, h=None):
    if password == adminpassword:
        return jsonify(login=True, flag=flag)
    else:
        return jsonify(login=False)

http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()

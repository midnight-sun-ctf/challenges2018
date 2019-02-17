#!/usr/bin/env python

from Crypto import Random
from Crypto.Cipher import AES

from flask import Flask, make_response, jsonify, request
app = Flask(__name__)


KEYS = {
    'e845799dc6bb731000221f5e20587814': '71554e5225a340a5e993c013d3aa5f0f'
}

# 4ecf769b12a9570eb30fbca73d6fc5a75ea4561928aba9a19e8556f4b32844ac
# 19c3fea9496e1de06487edd5d070dea1

@app.route('/')
def index():
    return app.send_static_file('index.html')

#@app.route("/key", methods=['POST'])
def key():
    try:
        print(request.json)
        key = request.json['key']
        keyid = request.json['id']
    except:
        return make_response(jsonify({
            'status': 'error',
            'message': 'malformed message'
        }), 400)

    KEYS[keyid] = key

    return make_response(jsonify({
        'status': 'ok',
        'message': 'key stored'
    }), 200)

@app.route("/key", methods=['POST'])
def key_broken():
    return make_response(jsonify({
        'status': 'error',
        'message': 'key store in read-only maintenance mode'
    }), 500)

@app.route("/data", methods=['POST'])
def data():
    try:
        print(request.json)
        ciphertext = request.json['ciphertext']
        keyid = request.json['keyid']
    except:
        return make_response(jsonify({
            'status': 'error',
            'message': 'malformed message'
        }), 400)

    if keyid not in KEYS:
        return make_response(jsonify({
            'status': 'error',
            'message': 'key not found'
        }), 404)

    key = KEYS[keyid]
    ciphertext = ciphertext.decode('hex')
    iv, ciphertext = ciphertext[:16], ciphertext[16:]
    aes = AES.new(key.decode('hex'), mode=AES.MODE_CBC, IV=iv)

    try:
        message = aes.decrypt(ciphertext)
        print(repr(message))
        if not all([c == message[-1] for c in message[-ord(message[-1]):]]):
            raise ValueError('Invalid padding')
        message = message[:-ord(message[-1])]
    except Exception as e:
        return make_response(jsonify({
            'status': 'error',
            'message': 'decryption failed'
        }), 400)

    print(repr(message))

    return make_response(jsonify({
        'status': 'ok',
        'message': 'message stored'
    }), 200)

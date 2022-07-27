import json
from flask import Flask, request, jsonify
import hmac
from hmac import compare_digest
from hashlib import sha256

app = Flask(__name__)

# INTERNAL TO API 
def get_shared_key():
    key_file = open('key.txt','r')
    key = bytes.fromhex(key_file.readline())
    return key

@app.route('/send-data',methods=['POST'])
def send():
    key = get_shared_key()
    data = json.dumps(request.json)
    hash_value = hmac.new(key,str.encode(data),digestmod=sha256).hexdigest()
    return jsonify({'hash':hash_value})

@app.route('/verify',methods=['POST'])
def verify():
    key = get_shared_key()
    data = request.json
    message = json.dumps(data['message'])
    hash_value = hmac.new(key,str.encode(message),digestmod=sha256).hexdigest()
    if compare_digest(hash_value,data['hash_value']):
        return "Message authenticated"
    else:
        return "Message is corrupted"

app.run()
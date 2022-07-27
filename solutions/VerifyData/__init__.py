import logging
import json
from flask import Flask, request, jsonify
import hmac
from hmac import compare_digest
from hashlib import sha256
import azure.functions as func

def get_shared_key():
    key_file = open('key.txt','r')
    key = bytes.fromhex(key_file.readline())
    return key

def main(req: func.HttpRequest) -> func.HttpResponse:
    key = get_shared_key()
    data = req.get_json()
    message = json.dumps(data['message'])
    hash_value = hmac.new(key,str.encode(message),digestmod=sha256).hexdigest()
    if compare_digest(hash_value,data['hash_value']):
        return func.HttpResponse("Message authenticated")
    else:
        return func.HttpResponse("Message is corrupted")

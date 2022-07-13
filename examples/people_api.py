import json
from flask import Flask, request, jsonify
import boto3
import pandas as pd
import hmac
import hashlib
from cryptography.fernet import Fernet
from secrets import token_hex
import jwt
from auth_middleware import token_is_required


aws_session = boto3.session.Session()
aws_secrets_client = aws_session.client(service_name='secretsmanager',region_name='us-west-2')

app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(16)


@app.route('/people_by_age/', methods=['GET'])
@token_is_required
def get_people_by_age(user_id):
    print(user_id)
    age = float(request.args.get('age'))
    dataset = pd.read_csv('demo.csv')
    dataset = dataset[dataset["Age"] >= age]
    return jsonify(dataset.to_dict(orient="records"))

@app.route('/add_person',methods=['POST'])
@token_is_required
def add_person():
    request_message = json.loads(request.data)
    hash_value,message = request_message
    key_bytes = aws_secrets_client.get_secret_value(SecretId='b21653e1-adb6-44ee-904e-46bb020b6608')['SecretBinary']
    
    symmetric_key_bytes = aws_secrets_client.get_secret_value(SecretId='b734211e-4eb9-49e2-b710-200ae6f457a1')['SecretBinary']
    fernet = Fernet(symmetric_key_bytes)

    #Recompute hash_value from encrypted message
    hmac_sha256_function = hmac.new(key_bytes, msg=bytes.fromhex(message),digestmod=hashlib.sha256)
    recomputed_hash = hmac_sha256_function.hexdigest()

    if hmac.compare_digest(recomputed_hash, hash_value):
        #Decrypt the ciphertext
        plaintext = fernet.decrypt(bytes.fromhex(message))
        message_dict =  json.loads(plaintext)
        dataset = pd.read_csv('demo.csv').append(message_dict,ignore_index=True)
        dataset.to_csv('demo.csv')
        return jsonify("Record created")
    else:
        return jsonify("Message authentication failed")


@app.route('/login',methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400

        if data["username"] == "admin" and data["password"] == "pass1234":
            data["token"] = jwt.encode({"user_id":data["username"]}, app.config["SECRET_KEY"],algorithm="HS256")
            return {
                "message": "Authentication successful",
                "data": data
            }
        else:
             return {
                "message": "Authentication failed",
                "data": None,
                "error": "Unauthorized"
            }, 404
    except Exception as e:
        print(e)
        return {
                "message": "A server error occurred",
                "data": None,
                "error": str(e)
            }, 500


app.run(debug=True)
    

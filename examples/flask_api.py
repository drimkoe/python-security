import json
import sqlite3
from flask import Flask,request,jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/',methods=['GET'])
def get_data_by_age():
    age = int(request.args.get('age'))
    dataset = pd.read_csv('demo.csv')
    dataset = dataset[dataset["Age"] >= age]
    return jsonify(dataset.to_dict(orient="records"))

app.run(debug=True)   
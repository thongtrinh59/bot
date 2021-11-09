from flask import Flask, jsonify, abort
# from flask_sqlalchemy import SQLAlchemy
import json
import requests


import os
import sys
from flask import request, g, jsonify





app = Flask(__name__)


@app.route('/')
def index():

    print("hello")
    return 200


# @app.route('/api')
# def internal():
#     print("api call")
#     return {"message": "An id does not exist"}, 404

@app.route('/api1')
def internal():
    print("internal")

    res = requests.get("http://project2_backend_1:5000/api")

    print(res.json())
    
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0')

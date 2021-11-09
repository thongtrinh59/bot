from flask import Flask, jsonify, abort, request, g
# from flask_sqlalchemy import SQLAlchemy
import json
import requests
from flask_cors import CORS, cross_origin


import os
import sys
# from flask import request, g, jsonify





app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    msg = request.args.get("message")
    return jsonify({"message":msg})




# @app.route('/api1')
# def internal():
#     print("internal")

#     res = requests.get("http://project2_backend_1:5000/api")

#     print(res.json())
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

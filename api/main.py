from flask import Flask, jsonify, abort, request, g
# from flask_sqlalchemy import SQLAlchemy
import json
import requests
from flask_cors import CORS, cross_origin
from wit import Wit


import os
import sys
# from flask import request, g, jsonify
from rivescript import RiveScript





app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = Wit("FXY4E2MNQBQ4VE3N3SUAIGJEJHOTYMRE")

# rs = RiveScript()
# rs.load_directory("./brain")
# rs.sort_replies()

@app.route('/')
@cross_origin()
def index():
    msg = request.args.get("message")
    resp = client.message(msg)
    print(resp)
    # reply = rs.reply("localuser", msg)
    return jsonify({"message":'reply'})
    
    # if resp['intents'][0]['id'] == '579324833351112':
    #     print(resp)
    #     return jsonify({"message":"Hi, nice to meet you"})
    # else:
    #     print(resp['intents'][0]['id'])
    #     return jsonify({"message":"msg"})




# @app.route('/api1')
# def internal():
#     print("internal")

#     res = requests.get("http://project2_backend_1:5000/api")

#     print(res.json())
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

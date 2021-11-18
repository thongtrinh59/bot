from flask import Flask, jsonify, abort, request, g
# from flask_sqlalchemy import SQLAlchemy
import json
import requests
from flask_cors import CORS, cross_origin
from wit import Wit
import random
import re


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

# global MOVIE_NAME
MOVIE_NAME = ""

@app.route('/')
@cross_origin()
def index():
    msg = request.args.get("message")
    resp = client.message(msg)
    print(resp)
    # greeting
    if resp['intents'][0]['name'] == 'greeting':
        list_of_rep = ['Hi! How are you doing?',
        'Hello! How can I help you?',
        'Good day! What can I do for you today?',
        'Greetings! How can I assist?']
        reply = random.choice(list_of_rep)
        return jsonify({"message":reply})
    elif resp['intents'][0]['name'] == 'SelectMovie':
        namem = resp['entities']['MovieName:MovieName'][0]['body']
        global MOVIE_NAME 
        if "\"" in namem:
            # print("OKKKKK")
            
            MOVIE_NAME = namem.strip("\"")
        else:
            # global MOVIE_NAME 
            MOVIE_NAME = namem
        print(MOVIE_NAME)
        list_of_ans = ["Good choice. ", "Great choice. ", "Excellet choice. "]
        list_of_rep = ['How can I help you next?',
        'What can I do for you next?',
        'How can I assist next?']
        rep1 = random.choice(list_of_ans)
        rep2 = random.choice(list_of_rep)
        print(rep1 + rep2)
        return jsonify({"message": rep1 + rep2})

    
    elif resp['intents'][0]['name'] == 'GetAllCinema':
        # headers = {'Content-Type' : 'application/json'}
        print("********************************************************")
        
        pr = {'status': 'available'}
        res = requests.get("http://project2_backend_1:5000/cinemas", params=pr)
        dict_result = json.loads(res.text)
        print(dict_result)
        print("********************************************************")
        name_of_avai_cinemas = []
        for _ in dict_result['return']:
            name_of_avai_cinemas.append(_['name'])
        answer = "This is the list of available cinemas for the movie:\n"
        for _ in name_of_avai_cinemas:
            answer += _ + ',\n'

        return jsonify({"message": answer})

    elif resp['intents'][0]['name'] == 'GetCinemaInfo':
        # print(res)
        namec = resp['entities']['CinemaName:CinemaName'][0]['body']
        print(namec)
        namecp = namec.lower()
        namec = namec.lower().replace(" ", "%20")
        print(namec)
        res = requests.get("http://project2_backend_1:5000/cinemas/{}".format(namec))

        print(res.text)
        ret = json.loads(res.text)
        rep_str = "The {} locate at {} with maximum capacity {}. The contact number is {}. ".format(
            ret['return'][0]['name'], ret['return'][0]['address'],
            ret['return'][0]['capacity'], ret['return'][0]['phone'])


        pr2 = {'status': 'now showing'}
        res2 = requests.get("http://project2_backend_1:5000/cinemas/movies", params=pr2)  
        ret2 = json.loads(res2.text)
        cinema2 = ret2['return']
        for _ in cinema2:
            if _.lower() == namecp:
                print(cinema2[_])
                list_str = ", ".join(cinema2[_])
        rep_str = rep_str + "The cinema is now showing " + list_str
        return jsonify({"message":rep_str})
    elif resp['intents'][0]['name'] == 'SearchCinemaByTitle':
        # headers = {'Content-Type' : 'application/json'}
        print("********************************************************")
        print(resp)
        namem = resp['entities']['MovieName:MovieName'][0]['body']
        if "\"" in namem:
            
            namem = namem.strip("\"")
        else:
            namem = namem
        pr = {'status': 'available', 'movie_title': f'{namem}'}
        res = requests.get("http://project2_backend_1:5000/cinemas", params=pr)
        dict_result = json.loads(res.text)
        print(dict_result)
        print("********************************************************")
        name_of_avai_cinemas = []
        for _ in dict_result['return']:
            name_of_avai_cinemas.append(_)
        answer = "This is the list of available cinemas for the movie {}:\n".format(namem)
        for _ in name_of_avai_cinemas:
            answer += _ + ',\n'
        return jsonify({"message": answer})

    elif resp['intents'][0]['name'] == 'CheckAvailableTS':
        print(resp)
    
        timerange = resp['entities']['wit$datetime:datetime'][0]['body']
        movie = resp['entities']['MovieName:MovieName'][0]['body']
        seats = resp['entities']['Seat:Seat'][0]['body']

        pattern = '\d+'
        result = re.findall(pattern, timerange)
        print(timerange)

        starttime = result[0] + ':00'
        endtime = result[1] + ':00'

        if "\"" in movie:
            
            movie = movie.strip("\"")
        else:
            movie = movie
        new_movie_name = movie.lower().replace(" ", "%20")
        p4 = {'status': 'available', 'starttime': starttime, 'endtime': endtime}
        res = requests.get(f"http://project2_backend_1:5000/movies/{new_movie_name}/timeslots", params=p4)
        dict_result = json.loads(res.text)

        cinemas = ""
        for _ in dict_result['return']['cinema']:
            cinemas += _['name'] + ', '


        try:
            if int(seats) <= dict_result['return']['total available']:
                rep = f"Yes, there are enough seats in the {cinemas}for the movie {dict_result['return']['movie name']} from {starttime} to {endtime}."
            else:
                rep = "not enough"
        except:
            pass
        return jsonify({"message": rep})


    else:
        return jsonify({"message":'reply'})
    





# @app.route('/api1')
# def internal():
#     print("internal")

#     res = requests.get("http://project2_backend_1:5000/api")

#     print(res.json())
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

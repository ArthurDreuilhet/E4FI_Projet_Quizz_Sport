from flask import Flask, request
from flask_cors import CORS
import hashlib

import jwt_utils

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    x = 'world'
    y = 'Why does Valentin say caca all the time?   Because he is a child at heart!'
    return f"Hello, {x}. {y}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def PostLogin():
    payload = request.get_json()

    if  hashlib.md5(payload['password'].encode('utf-8')).digest() == b'^\x92\xc9\xe1!\x18U\xd2tc\xfa\xc5c\xbepe' :
        token = jwt_utils.build_token()
        return {"status": "success", "token": f"{token}"}, 200
    else:
        return {"status": "Unauthorized", "message": "Invalid credentials", "indice": "Val"}, 401

if __name__ == "__main__":
    app.run()
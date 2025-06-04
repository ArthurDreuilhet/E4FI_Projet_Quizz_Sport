from flask import Flask, request
from flask_cors import CORS	
import hashlib
import jwt_utils

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'prou	t'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()

    if hashlib.md5(payload['password'].encode('utf-8')).digest() == b'^\x92\xc9\xe1!\x18U\xd2tc\xfa\xc5c\xbepe' :
        jwt_token = jwt_utils.build_token()
        return {"status": "success", "message": "Login successful", "token":jwt_token}, 200
    else:
        return {"status": "error", "message": "Invalid credentials"}, 401

@app.route('/post_question', methods=['POST'])
def PostQuestion():
    payload = request.get_json()
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return {"status": "error", "message": "Authorization header is missing"}, 401

    token = auth_header.split(" ")[1]
    try:
        user = jwt_utils.decode_token(token)
        # Here you would typically save the question to a database
        return {"status": "success", "message": "Question posted successfully"}, 200
    except jwt_utils.JwtError as e:
        return {"status": "error", "message": str(e)}, 401

if __name__ == "__main__":
    app.run()
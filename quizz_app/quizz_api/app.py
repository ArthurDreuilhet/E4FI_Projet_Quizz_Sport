from flask import Flask
from flask_cors import CORS

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

if __name__ == "__main__":
    app.run()
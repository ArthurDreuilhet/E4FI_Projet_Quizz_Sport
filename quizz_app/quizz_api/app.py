from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    x = 'world'
    y = 'Why does Valentin say caca all the time?'
    return f"Hello, {x}. {y}"

if __name__ == "__main__":
    app.run()
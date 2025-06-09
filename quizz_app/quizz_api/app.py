from flask import Flask, request
from flask_cors import CORS	
import hashlib
import jwt_utils
import sqlite3

def DBConnection():
    try:
        db_connection = sqlite3.connect('./bdd.db', timeout=10)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

    return db_connection

app = Flask(__name__)
CORS(app)

############################################################################    
#    
#   GENERAL ROUTES
#    
############################################################################  

@app.route('/')
def hello_world():
	x = 'World'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    score = []
    
    connection = DBConnection()
    if connection is None:
        return {"status": "error", "message": "Failed to connect to database"}, 500
    
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]
    
    cursor.execute("SELECT * FROM joueur")
    count_participants = cursor.fetchall()
        
    for participant in count_participants:
        print(f"[DEBUG] Participant: {participant[1]}, Score: {participant[2]}")
        score.append({
            "playerName": participant[1],
            "score": participant[2]
        })
    
    print(f"[DEBUG] Total number of questions: {score}")
    
    score = sorted(score, key=lambda x: x['score'], reverse=True)
    
    connection.commit()
    connection.close()
    
    return {"size": count, "scores": score}, 200

@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()

    if hashlib.md5(payload['password'].encode('utf-8')).digest() == b'^\x92\xc9\xe1!\x18U\xd2tc\xfa\xc5c\xbepe':
        jwt_token = jwt_utils.build_token()
        return {"status": "success", "message": "Login successful", "token": jwt_token}, 200
    else:
        return {"status": "error", "message": "Invalid credentials"}, 401
    
    
############################################################################    
#    
#   GESTION DES QUESTIONS
#    
############################################################################    

#############################################################   
#   
# POST

@app.route('/questions', methods=['POST'])
def PostQuestion():
    payload = request.get_json()
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return {"status": "error", "message": "Authorization header is missing"}, 401

    token = auth_header.split(" ")[1]
    try:
        user = jwt_utils.decode_token(token)        

        connection = DBConnection()

        if connection is None:
            return {"status": "error", "message": "Failed to connect to database"}, 500
        
        cursor = connection.cursor()

        print(f"[DEBUG] Authenticated user: {user}")
        
        cursor.execute("SELECT * FROM questions WHERE position=?", (payload['position'],))
        existing_question = cursor.fetchone()
        
        if existing_question:
            cursor.execute(
            "UPDATE questions SET position = position + 1 WHERE position >= ?",
            (payload['position'],)
        )

        cursor.execute(
            "INSERT INTO questions (position, content, title, image) VALUES (?, ?, ?, ?)",
            (payload['position'], payload['text'], payload['title'], payload['image'])
        )
        
        id_question = cursor.lastrowid        

        for answer in payload['possibleAnswers']:
            cursor.execute(
                "INSERT INTO reponses (correct, content, id_question) VALUES (?, ?, ?)",
                (answer['isCorrect'], answer['text'], id_question)
            )

        connection.commit()
        connection.close()

        return {"status": "success", "message": "Question posted successfully", "id":payload['position']}, 200
    
    except jwt_utils.JwtError as e:
        return {"status": "error", "message": str(e)}, 401

#############################################################   
#       
# GET
    
@app.route('/questions/<int:question_id>', methods=['GET'])
def GetQuestion(question_id):

    connection = DBConnection()

    if connection is None:
        return {"status": "error", "message": "Failed to connect to database"}, 500
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions WHERE id=?", (question_id,))
    question = cursor.fetchone()
    
    print (f"[DEBUG] Fetching question with ID: {question}")

    if not question:
        return {"status": "error", "message": "Question not found"}, 404

    cursor.execute("SELECT * FROM reponses WHERE id_question=?", (question_id,))
    responses = cursor.fetchall()

    print (f"[DEBUG] Fetching responses for question ID {question_id}: {responses}")

    connection.commit()
    connection.close()

    return {
        "status": "success",
        "id": question[0],
        "position": question[1],
        "text": question[2],
        "title": question[3],
        "image": question[4],
        "possibleAnswers": [
            {
                "text": response[2],
                "isCorrect": True if response[3] == 1 else False,
            } for response in responses
        ],
    }, 200
    
@app.route('/questions', methods=['GET'])
def Get_question_by_position():
    position = request.args.get('position', type=int)

    connection = DBConnection()

    if connection is None:
        return {"status": "error", "message": "Failed to connect to database"}, 500
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions WHERE position=?", (position,))
    
    question = cursor.fetchone()
    
    print(f"[DEBUG] Fetching question with position {position}: {question}")

    if not question:
        return {"status": "error", "message": "Question not found"}, 404

    cursor.execute("SELECT * FROM reponses WHERE id_question=?", (question[0],))
    responses = cursor.fetchall()

    connection.commit()
    connection.close()

    return {
        "status": "success",
        "id": question[0],
        "position": question[1],
        "text": question[2],
        "title": question[3],
        "image": question[4],
        "possibleAnswers": [
            {
                "text": response[2],
                "isCorrect": True if response[3] == 1 else False,
            } for response in responses
        ],
    }, 200
 
#############################################################   
#    
# PUT

@app.route('/questions/<int:question_id>', methods=['PUT'])
def Update_Question(question_id):
    payload = request.get_json()
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return {"status": "error", "message": "Authorization header is missing"}, 401

    token = auth_header.split(" ")[1]
    try:
        user = jwt_utils.decode_token(token)
        print(f"[DEBUG] Authenticated user: {user}")
    except jwt_utils.JwtError as e:
        return {"status": "error", "message": str(e)}, 401

    connection = DBConnection()

    if connection is None:
        return {"status": "error", "message": "Failed to connect to database"}, 500
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions WHERE id=?", (question_id,))
    
    question = cursor.fetchone()

    if not question:
        return {"status": "error", "message": "Question not found"}, 404
    
    cursor.execute("SELECT * FROM questions WHERE position=?", (payload['position'],))
    existing_question = cursor.fetchone()
    
    if existing_question and payload['position'] < question[1]:
        cursor.execute(
            "UPDATE questions SET position = position + 1 WHERE position >= ? AND position < ?",
            (payload['position'], question[1])
        )
    elif existing_question and payload['position'] > question[1]:
        cursor.execute(
            "UPDATE questions SET position = position - 1 WHERE position <= ? AND position > ?",
            (payload['position'], question[1])
        )

    cursor.execute(
        "UPDATE questions SET position=?, content=?, title=?, image=? WHERE id=?",
        (payload['position'], payload['text'], payload['title'], payload['image'], question_id)
    )

    cursor.execute("DELETE FROM reponses WHERE id_question=?", (question_id,))

    for answer in payload['possibleAnswers']:
        cursor.execute(
            "INSERT INTO reponses (correct, content, id_question) VALUES (?, ?, ?)",
            (answer['isCorrect'], answer['text'], question_id)
        )

    connection.commit()
    connection.close()

    return {"status": "success", "message": "Question updated successfully"}, 204

#############################################################   
#       
# DELETE

@app.route('/questions/all', methods=['DELETE'])
def Delete_Question():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return {"status": "error", "message": "Authorization header is missing"}, 401
    
    token = auth_header.split(" ")[1]
    try:
        user = jwt_utils.decode_token(token)
        print(f"[DEBUG] Authenticated user: {user}")
    except jwt_utils.JwtError as e:
        return {"status": "error", "message": str(e)}, 401
    
    connection = DBConnection()

    if connection is None:
        return {"status": "error", "message": "Failed to connect to database"}, 500
    
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM questions")
    cursor.execute("DELETE FROM reponses")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='questions'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='reponses'")

    connection.commit()
    connection.close()

    return {"status": "success", "message": "All questions deleted successfully"}, 204


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def Delete_Question_by_id(question_id):
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return {"status": "error", "message": "Authorization header is missing"}, 401
    
    token = auth_header.split(" ")[1]
    try:
        user = jwt_utils.decode_token(token)
        print(f"[DEBUG] Authenticated user: {user}")
    except jwt_utils.JwtError as e:
        return {"status": "error", "message": str(e)}, 401
    
    connection = DBConnection()

    if connection is None:
        return {"status": "error", "message": "Failed to connect to database"}, 500
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM questions WHERE id=?", (question_id,))
    
    existing_question = cursor.fetchone()
    
    if not existing_question:
        return {"status": "error", "message": "Question not found"}, 404
    
    print(f"[DEBUG] Deleting question with ID: {existing_question}")
    
    cursor.execute(
        "UPDATE questions SET position = position - 1 WHERE position >= ? ",
        (existing_question[1],)
    )    

    cursor.execute("DELETE FROM questions WHERE id=?", (question_id,))
    cursor.execute("DELETE FROM reponses WHERE id_question=?", (question_id,))

    connection.commit()
    connection.close()

    return {"status": "success", "message": "Question deleted successfully"}, 204


############################################################################    
#    
#   GENERAL ROUTES
#    
############################################################################ 

@app.route('/participations', methods=['POST'])
def Post_participant():
    
    playload = request.get_json()
    
    connection = DBConnection()
    if connection is None:
        return {"status": "error", "message": "Failed to connect to database"}, 500
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]
    
    if count != len(playload['answers']):
        return {"status": "error", "message": "Number of answers does not match the number of questions"}, 400
    
    cursor.execute(
        "INSERT INTO joueur (nom, score) VALUES (?, ?)",
        (playload['playerName'], 0)
    )
    
    for answer_postion in range(len(playload['answers'])):
        print(f"[DEBUG] Processing answer at position {answer_postion} : {playload['answers'][answer_postion]}")
        cursor.execute(
            "SELECT * FROM questions WHERE position=?",
            (answer_postion + 1,)
        )
        
        question = cursor.fetchone()
        
        print(f"[DEBUG] Fetching question with position {answer_postion + 1} : {question[1]}")
        
        if not question:
            return {"status": "error", "message": f"Question at position {playload['answers'][answer_postion] + 1} not found"}, 404
        
        cursor.execute(
            "SELECT * FROM reponses WHERE id_question=?",
            (question[0],)
        )
        
        reponses = cursor.fetchall()
        print(f"[DEBUG] Fetching responses for question ID {question[0]}: {reponses}")
        
        if not reponses:
            return {"status": "error", "message": f"No responses found for question at position {playload['answers'][answer_postion] + 1}"}, 404
        
        if (reponses[playload['answers'][answer_postion] - 1][3] == 1):
            cursor.execute(
                "UPDATE joueur SET score = score + 1 WHERE nom=?",
                (playload['playerName'],)
            )
            
    cursor.execute(
        "SELECT * FROM joueur WHERE nom=?",
        (playload['playerName'],)
    )
    participant = cursor.fetchone()
    if not participant:
        return {"status": "error", "message": "Participant not found"}, 404        
        
    connection.commit()
    connection.close()
    return {"status": "success", "message": "Participant added successfully", "playerName":participant[1], "score":participant[2]}, 200

@app.route('/participations/all', methods=['DELETE'])
def Delete_participant():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return {"status": "error", "message": "Authorization header is missing"}, 401
    
    token = auth_header.split(" ")[1]
    try:
        user = jwt_utils.decode_token(token)
        print(f"[DEBUG] Authenticated user: {user}")
    except jwt_utils.JwtError as e:
        return {"status": "error", "message": str(e)}, 401    
    
    connection = DBConnection()
    if connection is None:
        return {"status": "error", "message": "Failed to connect to database"}, 500
    
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM joueur")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='joueur'")
    
    connection.commit()
    connection.close()
    
    return {"status": "success", "message": "All participants deleted successfully"}, 204
    

if __name__ == "__main__":
    app.run()
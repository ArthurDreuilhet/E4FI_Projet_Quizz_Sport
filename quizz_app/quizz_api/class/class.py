class Question :
    def __init__(self, id : int, position : int, content : str, title : str, image : str):
        self.id = id
        self.position = position
        self.content = content
        self.title = title
        self.image = image

class Response :
    def __init__ (self, id : int, correct : int, content : str, question_id : int):
        self.id = id
        self.correct = correct
        self.content = content
        self.question_id = question_id
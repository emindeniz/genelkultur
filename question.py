from db import get_db

class Question():
    def __init__(self, id=None, question_text=None, answer=None, score=None, qtype=None, category=None):
        self.id = id
        self.question_text = question_text
        self.answer = answer
        self.score = score
        self.qtype = qtype
        self.category = category

    @staticmethod
    def get_random():
        db = get_db()
        question = db.execute(
            f"""
            SELECT top 1 * FROM [dbo].[questions] 
            WHERE id >= RAND() * (SELECT MAX(id) FROM [dbo].[questions])
            order by id;
            """
        ).fetchone()

        question = Question(
            id=question[0], 
            question_text=question[1], 
            answer=question[2], 
            score = question[3],
            qtype= question[4],
            category = question[5]
        )

        return question
    
    @staticmethod
    def get_question(question_id):
        db = get_db()
        question = db.execute(
            f"""
            SELECT * from [dbo].[questions] 
            WHERE id={question_id};
            """
        ).fetchone()

        question = Question(
            id=question[0], 
            question_text=question[1], 
            answer=question[2], 
            score = question[3],
            qtype= question[4],
            category = question[5]
        )

        return question
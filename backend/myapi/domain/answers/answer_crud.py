from datetime import datetime

from sqlalchemy.orm import Session

from domain.answers.answer_schema import AnswerCreate, AnswerUpdate
from models import Posts, Answers, Users

def create_answer(db: Session, post_id: int, answer_create: AnswerCreate, user: Users):#, user: Users):
    
    user_id = db.session.query(Users)
    db_answer = Answers(post_id = post_id,
                       content = answer_create.content,
                       create_date = datetime.now(), user = user)

    db.add(db_answer)
    db.commit()


#포스트 id와 같은 댓글 리스트 불러오기
def get_answers_list(db: Session, post_id: int):
    answers_list = db.query(Answers).filter(Posts.post_id == post_id).all()
    return answers_list
    
def update_answer(db: Session, db_answer: Answers,
                  answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit
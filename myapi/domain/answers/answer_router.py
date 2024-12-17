from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answers import answer_schema, answer_crud
from domain.posts import posts_crud
from domain.users.users_router import get_current_user
from models import Users

router = APIRouter(
    prefix = "/api/answer",
)

#입력: answer_schema.AnswerCreate , 출력: 없음
@router.post("/create/{post_id}", status_code = status.HTTP_204_NO_CONTENT) #204: 응답없음
def answer_create(post_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db),
                  current_user: Users = Depends(get_current_user)):
        #create answer

        post = posts_crud.get_post(db, post_id=post_id)
        if not post:
                raise HTTPException(status_code = 404, detail = "Post not found")
        answer_crud.create_answer(db, post_id = post_id,
                                  answer_create=_answer_create,
                                  user = current_user)

#answer_list
@router.post("/list", response_model = list[answer_schema.Answers])
def answer_list(post_id: int, db: Session = Depends(get_db)):
        _answer_list = answer_crud.get_answers_list(db, post_id=post_id)
        return _answer_list


@router.get("/detail/{answer_id}", response_model=answer_schema.Answers)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
        answer = answer_crud.get_answers_list(db, answer_id = answer_id)
        return answer


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                  db: Session = Depends(get_db),
                  current_user: Users = Depends(get_current_user)):
        db_answer = answer_crud.get_answers_list(db, answer_id = _answer_update.answer_id)
        if not db_answer:
                raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                                    detail="데이터를 찾을 수 없습니다.")
        if current_user.id != db_answer.user.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="수정 권한이 없습니다.")
        answer_crud.update_answer(db=db, db_answer=db_answer, answer_update=_answer_update)





#댓글 삭제

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                  db: Session = Depends(get_db),
                  current_user: Users = Depends(get_current_user)):
        db_answer = answer_crud.get_answers_list(db, answer_id=_answer_delete.answer_id)
        if not db_answer:
                raise HTTPException(status_codes= status.HTTP_400_BAD_REQUEST,
                                    detail="데이터를 찾을 수 없습니다.")
        if current_user.id != db_answer.users.id:
                raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                                    detail="삭제 권한이 없습니다.")
        answer_crud.delete_answer(db=db, db_answer=db_answer)
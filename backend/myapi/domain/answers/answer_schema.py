import datetime
from pydantic import BaseModel
from pydantic.functional_validators import field_validator
from domain.users.users_schema import Users


class Answers(BaseModel):
    answer_id: int | None  = None
    post_id: int | None  = None
    content: str
    create_date: datetime.datetime
    user: Users | None
    post_id: int


class AnswerCreate(BaseModel):
    
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    

class AnswerUpdate(AnswerCreate):
    answer_id: int
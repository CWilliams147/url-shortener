from fastapi import HTTPException, status, Query
from models.users import User, UserAccountSchema

from db import session
from config import settings

def create_user(user: UserAccountSchema):
    db_user = User(**user.model_dump())
    print(db_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user(email: str):
    print(email)
    return session.query(User).filter(User.email == email).one()
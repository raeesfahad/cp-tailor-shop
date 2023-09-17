from fastapi_login import LoginManager
from fastapi import APIRouter, HTTPException, Depends
from database.models import *
from database.connection import get_session
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from database.connection import engine


router = APIRouter(
    prefix="/api/user",
    tags=["users"])





SECRET = "d239259f330c25e9b433579cdaf05469391d826faf4c01f7"
manager = LoginManager(SECRET, "/login", use_cookie = True)


@manager.user_loader()
def query_loader(id : int):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == id))
        return user


@router.post("/login")
def Login(data : OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    with Session(engine) as session:
        query = session.exec(select(User).where(User.email == email))
        user = query.first()
        if not user:
            raise InvalidCredentialsException
        elif password != user.password:
            raise InvalidCredentialsException

        access_token = manager.create_access_token(
        data={'sub': email}
    )
    return {'access_token': access_token}




@router.post( '/add',  response_model=UserRead)
async def create_user(*, user : UserCreate,  session : Session = Depends(get_session)):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


from fastapi_login import LoginManager
from fastapi import APIRouter, HTTPException, Depends
from database.models import *
from database.connection import get_session
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from database.connection import engine


router = APIRouter(
    prefix="/api/auth",
    tags=["users"])





SECRET = "d239259f330c25e9b433579cdaf05469391d826faf4c01f7"
manager = LoginManager(SECRET, "/login")


@manager.user_loader()
def query_user(id : str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == id)).first()
        return user


@router.post("/login")
def Login(data : OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = query_user(email)
    if not user:
        raise "this with email"
    
    elif password != user.password:
        raise "this with pASSWORD"

    access_token = manager.create_access_token(
        data={'sub': email}
    )
    return {'access_token': access_token}




@router.post( '/create/user',  response_model=UserRead)
async def create_user(*, user : UserCreate,  session : Session = Depends(get_session)):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get('/user/current', response_model=UserRead)
async def getUser(email : str):
    user = query_user(email)
    return user
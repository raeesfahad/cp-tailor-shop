from fastapi.responses import JSONResponse
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
manager = LoginManager(SECRET, "/api/auth/login")


@manager.user_loader()
def query_user(id : str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == id)).first()
        return user


@router.post("/login")
def Login(data : OAuth2PasswordRequestForm = Depends()):
   

    user = query_user(data.username)
    if not user:
        raise "user not found"
    
    elif data.password != user.password:
        raise "user not found"

    access_token = manager.create_access_token(
        data={'sub': user.email}
    )
    return JSONResponse(content={"access_token" : access_token}, status_code=200)




@router.post( '/create/user',  response_model=UserRead)
async def create_user(*, user : UserCreate,  session : Session = Depends(get_session)):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user



@router.get('/user/current', response_model=UserRead)
async def getUser(currentUser : User = Depends(manager)):
    user = query_user(currentUser.email)
    return user
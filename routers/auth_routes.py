from auth import hash_password,verify_password,create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,APIRouter,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from models import Users
from schemas import User
router = APIRouter(prefix="/auth",tags=["Auths"])
@router.post("/register",status_code=201)
def register_user(user:User,db:Session=Depends(get_db)):
    hashed_password = hash_password(user.password)
    user_data = Users(
        email = user.email,
        hashed_password = hashed_password
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data
@router.post("/login",status_code=201)
def login_user(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(Users).filter(Users.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    valid = verify_password(form_data.password,user.hashed_password)
    if not valid:
        raise HTTPException(status_code = 401,detail="unauthorized")
    token = create_access_token({"sub":user.email})
    return {"access_token":token,"token_type":"bearer"}


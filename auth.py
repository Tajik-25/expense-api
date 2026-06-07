from passlib.context import CryptContext
from jose import jwt,JWTError,ExpiredSignatureError
from datetime import datetime,timedelta
from database import get_db
from models import Users
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends
from config import SECRET_KEY,ALGORITHM
oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(password:str):
    return pwd_context.hash(password)
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token
def decode_token(token:str):
    try:
        data = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="token expired")
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid token")
def get_current_user(token:str=Depends(oauth2scheme),db:Session=Depends(get_db)):
    payload = decode_token(token)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()
    return user

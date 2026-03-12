from jose import jwt,JWTError
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi import Depends,HTTPException
from datetime import datetime,timedelta
from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.table import User

security=HTTPBearer()
SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
EXP_TIME=settings.TOKEN_EXPIRE_TIME


def create_access_token(data:dict,db:Session):
    check=db.query(User).filter(User.email==data["sub"]).first()
    if check.is_verify!=True:
        raise HTTPException(status_code=401,detail="email didn't verified")
    to_encode=data.copy()
    exptime=datetime.utcnow()+timedelta(minutes=EXP_TIME)
    to_encode.update({"type":"access","exp":exptime})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def create_refresh_token(data:dict,db:Session):
    check=db.query(User).filter(User.email==data["sub"]).first()
    if check.is_verify!=True:
        raise HTTPException(status_code=401,detail="email didn't verified")
    to_encode=data.copy()
    exptime=datetime.utcnow()+timedelta(days=7)
    to_encode.update({"type":"refresh","exp":exptime})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token:HTTPAuthorizationCredentials=Depends(security)):
    try:
        playload=jwt.decode(token.credentials,SECRET_KEY,algorithms=[ALGORITHM])
        if playload["type"]!="access":
            raise HTTPException(status_code=401,detail="not an access token")
        return playload
    except JWTError:
        raise HTTPException(status_code=404,detail="wrong or expired token")

def verify_refresh_token(token:str):
    try:
        playload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if playload["type"]!="refresh":
            raise HTTPException(status_code=401,detail="not an access token")
        return playload
    except JWTError:
        raise HTTPException(status_code=404,detail="wrong or expired token")
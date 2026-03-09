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


def create_token(data:dict,db:Session):
    check=db.query(User).filter(User.email==data["sub"]).first()
    if check.is_verify!=True:
        raise HTTPException(status_code=401,detail="email didn't verified")
    to_encode=data.copy()
    exptime=datetime.utcnow()+timedelta(minutes=EXP_TIME)
    to_encode.update({"exp":exptime})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token:HTTPAuthorizationCredentials=Depends(security)):
    try:
        playload=jwt.decode(token.credentials,SECRET_KEY,algorithms=[ALGORITHM])
        return playload
    except JWTError:
        raise HTTPException(status_code=404,detail="wrong or expired token")


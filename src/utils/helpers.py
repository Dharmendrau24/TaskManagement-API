from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.user.models import UserModel
import jwt
from src.utils.db import get_db
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.utils.settings import settings
from src.user.models import UserModel

def is_authenticated(request:Request, db: Session = Depends(get_db)):
    try:
      token = request.headers.get("Authorization")
      if not token:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Authorization token is missing."
          )
      token = token.split(" ")[-1] 
      data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
      user_id = data.get("id")
      
      user = db.query(UserModel).filter(UserModel.id == user_id).first()
      if not user:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="User not found."
          ) 
      return user
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired."
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )
from fastapi import HTTPException,status, Request
from src.user.dtos import UserSchema
from src.user.models import UserModel
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from src.user.dtos import LoginSchema
from src.utils.settings import settings
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(body: UserSchema, db: Session):
    is_user = db.query(UserModel).filter(
        UserModel.username == body.username
    ).first()

    if is_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    is_email = db.query(UserModel).filter(
        UserModel.email == body.email
    ).first()

    if is_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    hashed_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        email=body.email,
        hash_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(
        UserModel.username == body.username
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You entered an invalid username."
        )
    if not verify_password(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You entered an invalid password."
        )
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"id":user.id, "exp": exp_time.timestamp()}, settings.SECRET_KEY, algorithm=settings.ALGORITHM, )
    return {"token": token}

## token send
def is_authenticated(request:Request, db: Session):
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
    

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta


from ATL.services import user as services
from ATL.dependencies import get_db
from ATL.schemas.user import UserCreate


from ATL.auth.auth_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/user")

@router.post("/login", tags=["User"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    authenticated = services.authenticate_user(db, form_data.username, form_data.password)
    if authenticated:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"name": form_data.username}
        token = create_access_token(data, access_token_expires)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    

@router.post("/register", tags=["User"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    if not services.is_name_already_registered(db, user.name):
        db_user = services.register_new_user(db, user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"name": db_user.name}
        token = create_access_token(data, access_token_expires)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Name already registered")

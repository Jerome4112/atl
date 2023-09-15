from sqlalchemy.orm import Session

from ATL.models.user import User
from ATL.schemas.user import  UserCreate
from ATL.auth.password_handler import verify_password, get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()

def authenticate_user(db: Session, name: str, password: str):
    db_user = get_user_by_name(db, name)
    if not db_user:
        return False
    else:
        return verify_password(password, db_user.hashed_password)

def is_name_already_registered(db: Session, name: str):
    db_user = get_user_by_name(db, name)
    if db_user:
        return True
    else:
        return False
    
def register_new_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = User(name=user.name, hashed_password=hashed_password, is_authorised=user.is_authorised)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from pydantic import BaseModel
#from ATL.schemas.comments import Comment


class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    hashed_password: str
    is_authorised: bool = True
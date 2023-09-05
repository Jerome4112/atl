from pydantic import BaseModel
#from ATL.schemas.posts import Post
#from ATL.schemas.comments import Comment


class CustomerBase(BaseModel):
    id : int


class CustomerCreate(CustomerBase):
    name: str
    employee: str
    adress: str
    adressNr: int
    email: str
    tel: int


class Customer(CustomerBase):
    id: int
    name: str
    employee: str
    adress: str
    adressNr: int
    email: str
    tel: int

    class Config:
        from_attributes = True
from pydantic import BaseModel
#from ATL.schemas.posts import Post
#from ATL.schemas.comments import Comment


class CustomerBase(BaseModel):
    id : int


class CustomerCreate(CustomerBase):
    name: str
    adress: str
    adressNr: int
    email: str
    tel: int
    city: str
    postalCode: int


class Customer(CustomerBase):
    id: int
    name: str
    adress: str
    adressNr: int
    email: str
    tel: int
    city: str
    postalCode: int

    class Config:
        from_attributes = True
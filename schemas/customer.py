from pydantic import BaseModel
#from ATL.schemas.posts import Post
#from ATL.schemas.comments import Comment


class CustomerBase(BaseModel):
    id : int


class CustomerCreate(CustomerBase):
    name: str


class Customer(CustomerBase):
    id: int
    name: str

    class Config:
        from_attributes = True
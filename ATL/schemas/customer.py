from pydantic import BaseModel
from ATL.schemas.employee import Employee
#from ATL.schemas.comments import Comment


class CustomerBase(BaseModel):
    id : int
    name: str


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

    employees: list[Employee] =[]

    class Config:
        from_attributes = True
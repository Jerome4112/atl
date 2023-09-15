from pydantic import BaseModel
from ATL.schemas.order import Order



class EmployeeBase(BaseModel):
    id: int
    first_name: str
    last_name: str



class EmployeeCreate(EmployeeBase):
    email: str
    passwordEmail: str
    tel: int


class Employee(EmployeeBase):
    id: int
    first_name: str
    last_name: str
    email: str
    passwordEmail:str
    tel: int
    orders: list[Order] =[]

class Employee_order(EmployeeBase):
    orders: list[Order] =[]
    
    class Config:
        from_attributes = True


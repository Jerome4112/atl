from pydantic import BaseModel
from ATL.schemas.order import Order



class EmployeeBase(BaseModel):
    first_name: str
    last_name: str



class EmployeeCreate(EmployeeBase):
    id: int
    email: str
    tel: int

class Employee_order(EmployeeBase):
    id: int
    orders: list[Order] =[]
    


class Employee(EmployeeBase):
    id: int
    first_name: str
    last_name: str
    email: str
    tel: int



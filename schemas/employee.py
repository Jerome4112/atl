from pydantic import BaseModel



class EmployeeBase(BaseModel):
    first_name: str
    last_name: str


class EmployeeCreate(EmployeeBase):
    id: int
    email: str
    tel: int


class Employee(EmployeeBase):
    id: int
    first_name: str
    last_name: str
    email: str
    tel: int
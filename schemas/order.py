from pydantic import BaseModel
from ATL.schemas.program import Program





class OrderBase(BaseModel):
    id: int
    title: str

class OrderCreate(OrderBase):
    hardware: str
    details: str

class Order(OrderBase):
    hardware: str
    details: str
    programs: list[Program] =[]

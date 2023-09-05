from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ATL.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    employee = Column(String, index=True)
    adress = Column(String, index=True)
    adressNr = Column(Integer, index=True)
    email = Column(String, index=True)
    tel = Column(Integer, index=True)

    


    
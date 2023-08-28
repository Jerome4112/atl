from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ATL.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, primary_key=True, index=True)

    


    
from sqlalchemy import Column, Integer, String
from sqlalchemy.ATL import relationship

from ATL.database import Base

class Company(Base, Customer):
    __tablename__ = "firma"

    id = Column(Integer, primary_key=True, index=True)
    firmenname = Column(String, unique=True, index=True)
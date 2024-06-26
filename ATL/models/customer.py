from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ATL.database import Base


class Customer(Base):
    __tablename__ = "customer"
    # Spalten der Tabelle Customer
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    adress = Column(String, index=True)
    adressNr = Column(Integer, index=True)
    email = Column(String, index=True)
    tel = Column(Integer, index=True)
    city = Column(String, index = True)
    postalCode = Column(Integer, index=True)

    # Beziehung zu den Mitarbeitern des Kunden
    employees = relationship("Employee", back_populates="customer")
    # Beziehung zu den Aufträgen des Kunden
    orders = relationship("Order", back_populates="customer")

    


    
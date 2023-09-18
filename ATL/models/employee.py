from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ATL.database import Base


class Employee(Base):
    __tablename__ = "employee"
    # Spalten der Tabelle Employee
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email=Column(String, index=True)
    passwordEmail=Column(String, index=True)
    tel=Column(Integer, index=True)
    # Fremdschlüsselbeziehung zum Kunden (Customer) durch customer_id
    customer_id = Column(Integer, ForeignKey("customer.id"))

    # Beziehung zum Kunden
    customer = relationship("Customer", back_populates="employees")
    # Beziehung zu den Aufträgen des Mitarbeiters
    orders = relationship("Order", back_populates="employee")
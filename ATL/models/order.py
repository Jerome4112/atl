from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ATL.database import Base

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    hardware = Column(String, index=True)
    details = Column(String, index=True)
    # Fremdschlüsselbeziehung zum zugehörigen Mitarbeiter (Employee) durch employee_id
    employee_id = Column(Integer, ForeignKey("employee.id"))
    # Fremdschlüsselbeziehung zum zugehörigen Kunden (Customer) durch customer_id
    customer_id = Column(Integer, ForeignKey("customer.id"))
    # Beziehung zum zugehörigen Kunden (Customer)
    customer = relationship("Customer", back_populates="orders")
    # Beziehung zum zugehörigen Mitarbeiter (Employee)
    employee = relationship("Employee", back_populates="orders")
    # Beziehung zu den Programmen (Program), die dieser Bestellung zugeordnet sind,
    # über die Tabelle "order_programs"
    programs = relationship("Program", secondary="order_programs", back_populates="orders")


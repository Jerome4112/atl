from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ATL.database import Base

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    hardware = Column(String, index=True)
    details = Column(String, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    customer_id = Column(Integer, ForeignKey("customer.id"))

    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Employee", back_populates="orders")
    programs = relationship("Program", secondary="order_programs", back_populates="orders")


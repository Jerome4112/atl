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

    #programs = relationship("Order", back_populates="programs")
    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Employee", back_populates="orders")

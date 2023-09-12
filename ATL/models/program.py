from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ATL.database import Base


class Program(Base):
    __tablename__ = "program"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    licenseKey = Column(String, index=True)
    version = Column(String, index=True)
    installLink = Column(String, index=True)
    orders = relationship("Order", secondary="order_programs", back_populates="programs")
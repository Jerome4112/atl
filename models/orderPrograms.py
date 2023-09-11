from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ATL.database import Base


class OrderPrograms(Base):
    __tablename__ = "order_programs"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    program_id = Column(Integer, ForeignKey("program.id"))
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ATL.database import Base


class OrderPrograms(Base):
    __tablename__ = "order_programs"
     # Primärschlüssel für die OrderPrograms-ID automatisch generieren
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    # Fremdschlüsselbeziehung zur Bestellung (Order) durch order_id
    order_id = Column(Integer, ForeignKey("order.id"))
    # Fremdschlüsselbeziehung zum Programm (Program) durch program_id
    program_id = Column(Integer, ForeignKey("program.id"))
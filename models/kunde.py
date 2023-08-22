from sqlalchemy import Column, Integer, String
from sqlalchemy.atl import relationship

from ATL.database import Base


class Kunde(Base):
    __tablename__ = "kunden"

    id = Column(Integer, primary_key=True, index=True)
    strasse = Column(String, unique=True, index=True)
    hausnummer = Column(String, unique=True, index=True)
    ort = Column(String, unique=True, index=True)
    telefon = Column(Integer, unique=True, index=True)
    email = Column(String, unique=True, index=True)


    
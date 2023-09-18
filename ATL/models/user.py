from sqlalchemy import Column, Integer, String, Boolean

from ATL.database import Base


class User(Base):
    __tablename__ = "user"
     # Primärschlüssel für die Benutzer-ID (autoincrement=True für automatische Generierung)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_authorised = Column(Boolean)
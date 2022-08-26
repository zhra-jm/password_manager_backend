from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from .database import Base


class MasterPassword(Base):
    __tablename__ = "master_password"

    id = Column(Integer, primary_key=True, index=True)
    master_password = Column(String)
    hint = Column(String)


class Password(Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    url = Column(String)

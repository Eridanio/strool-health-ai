from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    idade = Column(String)
    data = Column(String)   # ex: 25/03
    hora = Column(String)
    telefone = Column(String)
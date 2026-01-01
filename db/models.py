from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Rol(Base):
    __tablename__ = "rol"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    mail = Column(String, nullable=False, unique=True)
    cod_rol = Column(Integer, ForeignKey("rol.id"), nullable=False)

import uuid
from sqlalchemy import UUID, Column, String, DateTime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    username = Column(String, unique=True)
    password = Column(String, unique=True)

class Acceso(Base):
    __tablename__ = "acceso" #mayus y min tiene que ser todo igual
    id = Column(
        String,
        primary_key=True,
        # no hay un default...
        index=True
    )
    ultimo_login = Column(
        DateTime
    )

class CategoriaModel(Base):
    __tablename__ = "categoria"
    id = Column(
        UUID,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    nombre = Column(
        String
    )
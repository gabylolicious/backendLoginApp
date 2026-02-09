from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CADENA_CONEXION = "postgresql://videojuegos:videojuegos@localhost:5432/bd_videojuegos"

engine = create_engine(CADENA_CONEXION)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
# Esta función dependencia se ejecuta para cada endpoint que requiera el uso de la BD, e inicia una sesión con la BD.
# Cuando termine de ejecutarse, cierra la sesión / el canal de comunicación
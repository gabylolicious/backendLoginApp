from pydantic import BaseModel

class Videojuego(BaseModel):
    id : str | None = None
    nombre : str
    descripcion : str
    url_imagen : str
    categoria : "Categoria"
    class Config:
        from_attributes = True

class Categoria(BaseModel):
    id : str | None = None
    nombre: str
    videogames : list[Videojuego]
    class Config:
        from_attributes = True
        # para jalar los atributos automaticamente de la BD y convertirlos en JSON

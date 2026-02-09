from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .categorias import Categoria

class Videojuego(BaseModel):
    id : str | None = None
    nombre : str
    descripcion : str
    url_imagen : str
    categoria : Categoria

router = APIRouter(
    # El prefijo de la ruta
    prefix="/videojuegos",
    tags=["Videojuegos"]
)

videojuegos = []

@router.get("/")
async def list_videojuegos():
    return {
        "msg" : "",
        "data" : videojuegos
    }
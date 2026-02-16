from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .categorias import Categoria



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
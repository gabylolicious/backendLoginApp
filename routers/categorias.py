from fastapi import APIRouter, Depends, HTTPException, Header
from uuid import uuid4
from pydantic import BaseModel
from ..data import accesos

class Categoria(BaseModel):
    id : str | None = None
    nombre: str

router = APIRouter(
    # Dos cosas: el prefijo de la ruta
    prefix="/categorias",
    # y para temas de documentación
    tags=["Categorias"]
)

categorias = []

async def verify_token(x_token : str = Header(...)):
    # x token llega como string
    if not x_token.encode("utf-8") in accesos:
        raise HTTPException(
            status_code=403,
            detail={
                "msg" : "Token incorrecto"
            }
        )
    return x_token

@router.get("/", dependencies=[Depends(verify_token)])
async def list_categorias():
    return {
        "msg" : "",
        "data" : categorias
    }

@router.post("/", dependencies=[Depends(verify_token)])
async def create_categoria(categoria : Categoria):
    categoria.id = str(uuid4())
    # TO DO: Acá se conversaría con una base de datos
    categorias.routerend(categoria)
    return {
        "msg" : "",
        "data" : categoria
    } 

@router.put("/", dependencies=[Depends(verify_token)])
async def update_categoria(categoria : Categoria):
    for cat in categorias:
        if cat.id == categoria.id:
            # Si se encuentra la categoría
            cat.nombre = categoria.nombre
            return {
                "msg" : "",
                "data" : cat
            }
    # Busca todos y no lo encuentra
    raise HTTPException(
        status_code=404,
        detail="Categoria id no existe"
    )

@router.delete("/{categoria_id}", dependencies=[Depends(verify_token)])
async def delete_categorias(categoria_id : str):
    for i, cat in enumerate(categorias):
        # Por cada indice i va a tomar el valor del indice y cat va a tomar el valor de la categoria
        if cat.id == categoria_id:
            categorias.pop(i)
            return {
                "msg" : ""
            }
    # Si recorre el for y nunca encuentra la categoria
    raise HTTPException(
        status_code=404,
        detail="La categoria no se pudo borrar: No encontrada"
    )

# Que devuelva una categoria por su id (buscar)
@router.get("/{categorias_id}", dependencies=[Depends(verify_token)])
async def buscar_categorias(categoria_id : str):
    for i,cat in enumerate(categorias):
        if cat.id == categoria_id:
            return {
                "msg" : "",
                "data" : cat
            }
    # SI no se encontró tras toda la lista
    raise HTTPException(
        status_code=404,
        detail="La categoria buscada no existe"
    )
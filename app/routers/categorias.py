import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from uuid import uuid4
from pydantic import BaseModel
from app.data import accesos
from sqlalchemy.orm import Session, selectinload
from ..database import get_db
from ..models import Acceso, CategoriaModel # .. para retroceder 1 nivel
from ..schemas import Categoria

router = APIRouter(
    # Dos cosas: el prefijo de la ruta
    prefix="/categorias",
    # y para temas de documentación
    tags=["Categorias"]
)

categorias = []

async def verify_token(x_token : str = Header(...), db : Session = Depends(get_db)):
    db_query = db.query(Acceso).filter(Acceso.id == x_token)
    db_acceso = db_query.first()
    
    if not db_acceso:
        raise HTTPException(
            status_code=403,
            detail={
                "msg" : "Token incorrecto"
            }
        )
    
    # Si llega hasta acá hubo acceso
    db_query.update({
        "ultimo_login" : datetime.datetime.now()
    })
    db.commit()
    db.refresh(db_acceso)

    return x_token

@router.get("/", dependencies=[Depends(verify_token)])
async def list_categorias(db : Session = Depends(get_db)):
    lista = db.query(CategoriaModel).options (
        selectinload(CategoriaModel.videojuegos)
    ).all()

    return {
        "msg" : "",
        "data" : lista
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
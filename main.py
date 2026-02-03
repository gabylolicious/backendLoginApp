from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

class LoginRequest(BaseModel):
    username : str = Field(...,min_length=5)
    password : str = Field(...,min_length=8)

class Categoria(BaseModel):
    id : str | None = None
    nombre: str

class Videojuego(BaseModel):
    id : str | None = None
    nombre : str
    descripcion : str
    url_imagen : str
    categoria : Categoria

categorias = []

@app.post("/login")
async def login(login_request : LoginRequest):
    if login_request.username == "PROGRAWEB" and login_request.password == "123123123":
        return{
            "msg" : "Acceso concedido"
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail="Error en login, credenciales incorrectas"
            )

@app.get("/categorias")
async def list_categorias():
    return {
        "msg" : "",
        "data" : categorias
    }

@app.post("/categorias")
async def create_categoria(categoria : Categoria):
    categoria.id = str(uuid4())
    # TO DO: Acá se conversaría con una base de datos
    categorias.append(categoria)
    return {
        "msg" : "",
        "data" : categoria
    } 

@app.put("/categorias")
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

@app.delete("/categorias/{categoria_id}")
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
@app.get("/categorias/{categorias_id}")
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
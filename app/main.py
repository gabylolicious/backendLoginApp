import time
import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from .routers.categorias import categorias
from .routers.videojuegos import videojuegos
from .data import accesos
# . = si es al mismo nivel
# .. = un nivel más arriba
from .database import get_db
from sqlalchemy.orm import Session
from .models import Usuario

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

@app.post("/login")
async def login(login_request : LoginRequest, db:Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.username==login_request.username,
        Usuario.password==login_request.password
    ).first() 
    # Devuelve un usuario que cumple con esas condiciones
    # Si no,
    if not usuario:
        raise HTTPException(
            status_code=400, 
            detail="Error en login, credenciales incorrectas"
        )
    
    hora_actual = time.time.ns()
    cadena_a_encriptar = f"{login_request.username}-{str(hora_actual)}"
    cadena_hasheada = bcrypt.hashpw(
        cadena_a_encriptar.encode("utf-8"),
        bcrypt.gensalt()
        ) # Esta es una cadena de bytes
    # Una vez el token creado
    #accesos[cadena_hasheada] = {
    #    "ultimo_login" : time.time.ns()
    #}

    return{
        "msg" : "Acceso concedido",
        "token" : cadena_hasheada
    }


    # if login_request.username == "PROGRAWEB" and login_request.password == "123123123":
    #     hora_actual = time.time.ns()
    #     cadena_a_encriptar = f"{login_request.username}-{str(hora_actual)}"
    #     cadena_hasheada = bcrypt.hashpw(
    #         cadena_a_encriptar.encode("utf-8"),
    #         bcrypt.gensalt()
    #     ) # Esta es una cadena de bytes
    #     # Una vez el token creado
    #     accesos[cadena_hasheada] = {
    #         "ultimo_login" : time.time.ns()
    #     }

    #     return{
    #         "msg" : "Acceso concedido",
    #         "token" : cadena_hasheada
    #     }
    # else:
    #     raise HTTPException(
    #         status_code=400, 
    #         detail="Error en login, credenciales incorrectas"
    #         )

@app.get("/logout")
async def logout(token : str):
    if token.encode("utf-8") in accesos:
        # Si está en la lista de accesos lo sacamos, sino nada
        accesos.pop(token.encode("utf-8"))
        return {
            "msg" : ""
        }
    else:
        return {
            "msg" : "Token no existe"
        }
app.include_router(categorias.router)
app.include_router(videojuegos.router)

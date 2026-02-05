import time
import bcrypt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from .routers import categorias, videojuegos
from .data import accesos
# . = si es al mismo nivel
# .. = un nivel más arriba

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
async def login(login_request : LoginRequest):
    if login_request.username == "PROGRAWEB" and login_request.password == "123123123":
        hora_actual = time.time.ns()
        cadena_a_encriptar = f"{login_request.username}-{str(hora_actual)}"
        cadena_hasheada = bcrypt.hashpw(
            cadena_a_encriptar.encode("utf-8"),
            bcrypt.gensalt()
        ) # Esta es una cadena de bytes
        # Una vez el token creado
        accesos[cadena_hasheada] = {
            "ultimo_login" : time.time.ns()
        }

        return{
            "msg" : "Acceso concedido",
            "token" : cadena_hasheada
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail="Error en login, credenciales incorrectas"
            )



app.include_router(categorias.router)
app.include_router(videojuegos.router)

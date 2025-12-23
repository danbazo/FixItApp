from fastapi import Body, FastAPI,status,HTTPException,Response, Depends
from typing import Optional,  List

from pydantic import BaseModel

app=FastAPI()

class Direccion(BaseModel):
    id:int
    calle:str
    alura:int
    codigoPostal:str
    localidad:str
    ciudad:str
    provincia:str 

class Usuario(BaseModel):
    id: int
    nombre: str
    apellido:str
    email:str
    esTec:bool
    direcciones:List[Direccion]
    numeroTel:int

class Rubro(BaseModel):
    id: int
    nombre: str
    descripcion:str
    requierCert:bool
    validado:bool
    

class Tecnico(BaseModel):
    id: int
    idUsuario:int
    descripcion:str
    rubros: List[Rubro]
    zonasDeTrabajo: List[str]
    clasificacion:float

class Trabajo(BaseModel):
    id:int
    idUsuario:int
    descripcion:str
    idRubro:int
    estatus:str #va a ser una seleccion de opciones

class Oferta(BaseModel):
    id:int
    idTrabajo:int
    idTecnico:int
    descripcion:str
    costo:float
    estatus:str #va a ser una seleccion de opciones

class Resena(BaseModel):
    id:int
    idOferta:int
    puntuacion:int #de 1 a 5
    comentario:str


@app.get("/health")
def health():
    return {"status": "ok"}
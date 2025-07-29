from fastapi import APIRouter, status, HTTPException
from typing import List
from database import conectar
from slugify import slugify
from esquema import *
from modelos import *


api = APIRouter()

@api.get("/categorias", response_model=List[CategoriaEsquema], status_code=status.HTTP_200_OK)
async def categorias():
    return conectar.execute(categorias_model.select().order_by(categorias_model.c.id.desc())).fetchall()


@api.get("/categorias/{id}", response_model=CategoriaEsquema, status_code=status.HTTP_200_OK)
async def categorias_get(id:int):

    datos = conectar.execute(categorias_model.select().where(categorias_model.c.id==id)).first()
    
    if datos:
        return datos
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultado en las categorias.")



@api.post("/categorias", response_model=ResponseEsquema, status_code=status.HTTP_201_CREATED)
async def categorias_post(model:CategoriaCrearEsquema):
    try:
        conectar.execute(categorias_model.insert().values({"nombre": model.nombre, "slug": slugify(model.nombre)}))
        return {"mensaje": "Se creó el registro exitosamente"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ocurrio un error inesperado")
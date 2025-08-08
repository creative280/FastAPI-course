from fastapi import APIRouter, status, HTTPException
from typing import List
from database import conectar
from slugify import slugify
from esquema import *
from modelos import *


api = APIRouter()

# ================================ CATEGORIAS ================================

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


@api.put("/categorias/{id}", response_model=ResponseEsquema, status_code=status.HTTP_200_OK)
async def categorias_put(id:int, model:CategoriaCrearEsquema):
    datos = conectar.execute(categorias_model.select().where(categorias_model.c.id==id)).first()    
    if datos:
        conectar.execute(categorias_model.update().values(nombre=model.nombre, slug=slugify(model.nombre)).where(categorias_model.c.id==id))
        return {"mensaje": "Se modifico correctamente el registro"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultado en las categorias.")


@api.delete("/categorias/{id}", response_model=ResponseEsquema, status_code=status.HTTP_200_OK)
async def categorias_delete(id:int, model:CategoriaCrearEsquema):
    datos = conectar.execute(categorias_model.select().where(categorias_model.c.id==id)).first()    
    if datos:
        existe = conectar.execute(productos_model.select().where(productos_model.c.categorias_id==id)).first()
        if existe:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar la categoria, tiene productos asociados.")
        else:
            conectar.execute(categorias_model.delete().where(categorias_model.c.id==id))
        return {"mensaje": "Se Elimino correctamente el registro"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultado en las categorias.")



# ================================ PRODUCTOS ================================

@api.get("/productos", response_model=List[ProductoEsquema], status_code=status.HTTP_200_OK)
async def productos():
    return conectar.execute(productos_model.select().order_by(productos_model.c.id.desc())).fetchall()



@api.get("/productos/{id}", response_model=ProductoEsquema, status_code=status.HTTP_200_OK)
async def productos_get(id:int):

    datos = conectar.execute(productos_model.select().where(productos_model.c.id==id)).first()
    
    if datos:
        return datos
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultado en los Productos.")


@api.post("/productos", response_model=ResponseEsquema, status_code=status.HTTP_201_CREATED)
async def productos_post(model:ProductoEsquema):
    try:
        conectar.execute(productos_model.insert().values({"nombre": model.nombre, "slug": slugify(model.nombre), "descripcion": model.descripcion, "precio": model.precio, "categorias_id": model.categorias_id}))
        return {"mensaje": "Se creó el registro exitosamente"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ocurrio un error inesperado")

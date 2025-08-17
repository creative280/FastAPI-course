import stat
from database import conectar
from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from datetime import datetime
from typing import List
from slugify import slugify
from esquema import *
from modelos import *
from utilidades import *
import os


# El api router me permite crear diferentes archivos para tener mis archivos separados, debo impotarlo en mi main.py
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



@api.delete("/productos/{id}", response_model=ResponseEsquema, status_code=status.HTTP_200_OK)
async def productos_delete(id:int):
    datos = conectar.execute(productos_model.select().where(productos_model.c.id==id)).first()
    print(datos)
    if datos:
        existe = conectar.execute(productos_fotos_model.select().where(productos_fotos_model.c.productos_id==id)).first()
        if existe:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar el producto, tiene compras asociadas.")
        else:
            conectar.execute(productos_model.delete().where(productos_model.c.id==id))
        return {"mensaje": "Se Elimino correctamente el registro"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultado en los productos.")


# ================================ PRODUCTOS CATEGORIA ================================


@api.get("/productos-categoria/{id}", response_model=List[ProductoEsquema], status_code=status.HTTP_200_OK)
async def productos_categoria(id: int):
    cat = conectar.execute(categorias_model.select().where(categorias_model.c.id==id)).first()
    if cat:
        datos = conectar.execute(productos_model.select().where(productos_model.c.categorias_id==id)).fetchall()
        return datos
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultado en las categorias.")


@api.post("/productos-fotos", response_model=ResponseEsquema, status_code=status.HTTP_201_CREATED)
async def productos_fotos_post(foto: UploadFile, productos_id: int = Form(...)):
    if getExtension(foto.content_type) == "No":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El archivo debe ser JPG o PNG"
        )

    # Verificar existencia del producto
    producto = conectar.execute(
        productos_model.select().where(productos_model.c.id == productos_id)
    ).first()
    if not producto:
        raise HTTPException(status_code=404, detail="El producto no existe")

    nombre = f"{datetime.timestamp(datetime.now())}{getExtension(foto.content_type)}"
    file_name = os.path.join(os.getcwd(), "assets", "productos", nombre)

    with open(file_name, "wb") as f:
        f.write(foto.file.read())

    conectar.execute(
        productos_fotos_model.insert().values(
            {"nombre": nombre, "productos_id": productos_id}
        )
    )
    conectar.commit()
    conectar.close()

    return {"mensaje": "Se creó el registro exitosamente"}


# ================================ PRODUCTOS FOTOS ================================


@api.get("/productos-fotos/{id}", response_model=List[ProductosFotoEsquema], status_code=status.HTTP_200_OK)
async def productos_fotos_por_producto(id:int):
    return conectar.execute(productos_fotos_model.select().where(productos_fotos_model.c.productos_id==id)).fetchall()


@api.get("/productos-fotos-render/{id}", status_code=status.HTTP_200_OK, response_description="Retorna la ruta de la foto")
async def productos_fotos_render(id:int):
    datos = conectar.execute(productos_fotos_model.select().where(productos_fotos_model.c.id==id)).first()
    if datos:
        return FileResponse(os.getcwd()+"/assets/productos/"+datos.nombre)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultado en las fotos.")


@api.delete("/productos-fotos-delete/{id}", response_model=ResponseEsquema, status_code=status.HTTP_200_OK)
async def productos_fotos_delete(id:int):
    datos = conectar.execute(productos_fotos_model.select().where(productos_fotos_model.c.id==id)).first()
    if datos:
        os.remove(os.getcwd()+"/assets/productos/"+datos.nombre)
        conectar.execute(productos_fotos_model.delete().where(productos_fotos_model.c.id==id))
        return {"mensaje": "Se Elimino correctamente el registro"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultado en las fotos.")



# ================================ PERFILES ================================


@api.get("/perfiles", response_model=List[PerfilEsquema], status_code=status.HTTP_200_OK)
async def perfiles():
    return conectar.execute(perfil_model.select().order_by(perfil_model.c.id.desc())).fetchall()


@api.get("/perfiles/{id}", response_model=PerfilEsquema, status_code=status.HTTP_200_OK)
async def perfiles_get(id: int):
    datos = conectar.execute(perfil_model.select().where(perfil_model.c.id==id)).first()
    if datos:
        return datos
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultados.")
        

@api.post("/perfiles", response_model=ResponseEsquema, status_code=status.HTTP_201_CREATED)
async def perfiles_post(model:PerfilEsquema):
    try:
        conectar.execute(perfil_model.insert().values({"nombre": model.nombre}))
        # conectar.commit()
        # conectar.close()
        return {"mensaje": "Se creo el registro correctamente"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin Resultados.")




# ================================ USUARIOS ================================
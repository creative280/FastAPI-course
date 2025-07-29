from pydantic import BaseModel
from typing import Optional


class CategoriaEsquema(BaseModel):
    id:Optional[int]
    nombre: str
    slug: Optional[str]

    class Config:
        schema_extra={
            "ejemplo": {
                "nombre": "Categoria 1",  
            }
        }


class ProductoEsquema(BaseModel):
    id:Optional[int]
    nombre: str
    slug: Optional[str]
    descripcion: str
    precio: int
    categorias_id: int

    class Config:
        schema_extra={
            "ejemplo": {
                "nombre": "Producto_Prueba",
                "descripcion": "Descripcion Producto Prueba",
                "precio": 1,
                "categorias_id": 1
            }
        }

class ProductosFotoEsquema(BaseModel):
    id: Optional[str]
    nombre: str
    productos_id: int

class LoginEsquema(BaseModel):
    correo: str
    password: str

    class Config:
        schema_extra={
            "Ejemplo":{
                "correo": "Prueba@gmail.com",
                "password": "123456"
            }
        }

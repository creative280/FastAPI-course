from fastapi import FastAPI, Form
from pydantic import BaseModel
from api import api

app = FastAPI()

# Incluir el router de api.py
app.include_router(api)


@app.get("/ejemplo")
async def ejemplo():
    return "Metodo GET"

@app.get("/ejemplo/{id}")
async def ejemplo_id(id:int):
    return f"Metodo GET | Parametro = {type(id)} | El Valor es = {id}"

@app.get("/ejemplo-query")
async def ejemplo_query(id, slug):
    return f"id={id} y el Slug = {slug}"

@app.post("/ejemplo-form")
async def ejmeplo_post(correo: str=Form(), password:str=Form()):
    
    return {"Correo": correo, "Password": password}


# @app.post("/ejemplo-request")
# async def ejmeplo_request(model:LoginEsquema):
#    return model


@app.put("/ejemplo")
async def ejmeplo_put():
    return "Metodo PUT"



@app.delete("/ejemplo")
async def ejmeplo_delete():
    return "Metodo DELETE"
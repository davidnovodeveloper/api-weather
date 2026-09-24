from fastapi import FastAPI, HTTPException
from utilities import obtener_clima
from models import Clima

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Servidor de clima funcionando"}

@app.get("/clima/{ciudad}")
def clima_por_ciudad(ciudad: str):
    resultado = obtener_clima(ciudad)

    if resultado is None:
        raise HTTPException(status_code=503, detail=f"No se pudo obtener el clima de {ciudad}")

    return Clima(**resultado)
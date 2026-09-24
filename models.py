from pydantic import BaseModel

class Clima(BaseModel):
    ciudad: str
    pais: str
    temperatura: float
    sensacion_termica: float
    humedad: int
    descripcion: str
    viento_kmh: float
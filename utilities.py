import os
import requests
import logging
from dotenv import load_dotenv
import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("weather.log", encoding="utf-8")
    ]
)

CLAVE_API = os.getenv("OPENWEATHER_API_KEY")

def obtener_clima(ciudad):

    clave_cache = f"clima:{ciudad}"

    try:
        en_cache = r.get(clave_cache)
    except redis.exceptions.RedisError as e:
        logging.warning(f"No se pudo leer de Redis, se continúa sin caché: {e}")
        en_cache = None

    if en_cache is not None:
        logging.info(f"Clima de {ciudad} servido desde caché")
        return json.loads(en_cache)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={CLAVE_API}&units=metric"

    try: 
        respuesta = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error de conexión al pedir clima de {ciudad}: {e}")
        return None

    if respuesta.status_code != 200:
        logging.warning(f"Status code inesperado ({respuesta.status_code}) para {ciudad}")
        return None
    datos = respuesta.json()

    resultado = {
                "ciudad": datos["name"],
        "pais": datos["sys"]["country"],
        "temperatura": datos["main"]["temp"],
        "sensacion_termica": datos["main"]["feels_like"],
        "humedad": datos["main"]["humidity"],
        "descripcion": datos["weather"][0]["description"],
        "viento_kmh": round(datos["wind"]["speed"] * 3.6, 1),
    }

    try:
        r.set(clave_cache, json.dumps(resultado), ex=600)
    except redis.exceptions.RedisError as e:
        logging.warning(f"No se puedo guardar en Redis: {e}")

    return resultado
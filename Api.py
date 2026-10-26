
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI


# Ruta del modelo entrenado
RUTA_MODELO = Path(__file__).resolve().parent / "modelo.joblib"

# Variable donde se guardara el modelo
modelo = None


# Cargar el modelo una sola vez al iniciar la API
@asynccontextmanager
async def lifespan(app: FastAPI):
    global modelo
    modelo = joblib.load(RUTA_MODELO)
    app.state.modelo = modelo
    yield


# Crear la API REST
app = FastAPI(
    title="API Detector de Intrusiones",
    description="API REST para integrar el detector de intrusiones con IA",
    version="1.0.0",
    lifespan=lifespan
)


# Endpoint para comprobar el estado de la API
@app.get("/salud")
def salud():
    return {
        "estado": "ok",
        "modelo_cargado": modelo is not None
    }

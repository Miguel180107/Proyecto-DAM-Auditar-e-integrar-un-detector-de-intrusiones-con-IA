
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI

from pydantic import BaseModel
from typing import List

from logtools import cargar_lineas, construir_features



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

class PeticionAnalisis(BaseModel):
    lineas: List[str]
    umbral: float = 0.7
    lista_blanca: List[str] = []


# Endpoint para comprobar el estado de la API
@app.get("/salud")
def salud():
    return {
        "estado": "ok",
        "modelo_cargado": modelo is not None
    }



@app.post("/analizar")
def analizar(datos: PeticionAnalisis):

    if datos.umbral < 0 or datos.umbral > 1:
        return {
            "error": "El umbral debe estar entre 0 y 1"
        }

    df, ignoradas = cargar_lineas(datos.lineas)

    if len(df) == 0:
        return {
            "error": "No se encontraron eventos válidos"
        }

    X = construir_features(df)



    probabilidades = app.state.modelo.predict_proba(X)[:,1]

    sospechosas = []

    for ip, prob in zip(X.index, probabilidades):

        if ip in datos.lista_blanca:
            continue

        if prob >= datos.umbral:

            sospechosas.append({
                "ip": ip,
                "probabilidad": round(float(prob), 4),
                "motivo": "Probabilidad superior al umbral"
            })


    return {
        "ips_analizadas": len(X),
        "lineas_ignoradas": ignoradas,
        "sospechosas": sospechosas
    }

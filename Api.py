

from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from logtools import cargar_lineas, construir_features


# Ruta del modelo entrenado
RUTA_MODELO = Path(__file__).resolve().parent / "modelo.joblib"

# Variable donde se guardará el modelo
modelo = None

# Número máximo de líneas permitidas por petición
MAX_LINEAS = 10000


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


# Datos que recibirá el endpoint /analizar
class PeticionAnalisis(BaseModel):
    lineas: List[str]
    umbral: float = 0.7
    lista_blanca: List[str] = Field(default_factory=list)


# Endpoint para comprobar el estado de la API
@app.get("/salud")
def salud():
    return {
        "estado": "ok",
        "modelo_cargado": modelo is not None
    }


# Endpoint para analizar el log
@app.post("/analizar")
def analizar(datos: PeticionAnalisis):

    # Comprobar el número de líneas recibidas
    if len(datos.lineas) > MAX_LINEAS:
        raise HTTPException(
            status_code=422,
            detail="El log no puede superar las 10000 líneas"
        )

    # Comprobar que el umbral está entre 0 y 1
    if not 0 <= datos.umbral <= 1:
        raise HTTPException(
            status_code=422,
            detail="El umbral debe estar entre 0 y 1"
        )

    # Comprobar que se han enviado líneas
    if not datos.lineas or all(not linea.strip() for linea in datos.lineas):
        raise HTTPException(
            status_code=422,
            detail="El log está vacío"
        )

    # Procesar las líneas del log
    try:
        df, ignoradas = cargar_lineas(datos.lineas)
    except (ValueError, TypeError) as error:
        raise HTTPException(
            status_code=422,
            detail=f"No se pudo procesar el log: {error}"
        )

    # Comprobar que hay eventos reconocibles
    if df is None or len(df) == 0:
        raise HTTPException(
            status_code=422,
            detail="No se encontraron eventos válidos en el log"
        )

    # Obtener las características de cada IP
    X = construir_features(df)

    if X is None or len(X) == 0:
        raise HTTPException(
            status_code=422,
            detail="No se pudieron extraer características de las IP"
        )

    # Calcular la probabilidad de que cada IP sea atacante
    probabilidades = app.state.modelo.predict_proba(X)[:, 1]

    sospechosas = []
    lista_blanca = set(datos.lista_blanca)

    # Revisar cada IP y aplicar el umbral y la lista blanca
    for ip, prob in zip(X.index, probabilidades):

        ip = str(ip)

        # Las IP de la lista blanca nunca se marcan
        if ip in lista_blanca:
            continue

        # Solo se incluyen las IP que alcanzan el umbral
        if prob >= datos.umbral:

            # Crear un motivo inicial para la sospecha
            motivo = "Probabilidad superior o igual al umbral"

            sospechosas.append({
                "ip": ip,
                "probabilidad": round(float(prob), 4),
                "motivo": motivo
            })

    # Devolver el resultado del análisis
    return {
        "ips_analizadas": len(X),
        "lineas_ignoradas": int(ignoradas),
        "sospechosas": sospechosas
    }


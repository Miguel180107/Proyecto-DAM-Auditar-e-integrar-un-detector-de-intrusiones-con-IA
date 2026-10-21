from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI


# Buscar el modelo en la carpeta del proyecto
RUTA_MODELO = Path(__file__).resolve().parent / "modelo.joblib"


# Cargar el modelo una sola vez al arrancar
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not RUTA_MODELO.exists():
        raise RuntimeError(
            "No se encuentra modelo.joblib. "
            "Primero debes entrenar el modelo."
        )

    app.state.modelo = joblib.load(RUTA_MODELO)
    yield


# Crear la API REST
app = FastAPI(
    title="Detector de intrusiones",
    description="API para consultar el estado del detector",
    version="1.0.0",
    lifespan=lifespan
)


# Comprobar que la API funciona
@app.get("/salud")
def salud():
    modelo = app.state.modelo

    caracteristicas = getattr(modelo, "feature_names_in_", [])
    numero = getattr(modelo, "n_features_in_", None)

    return {
        "estado": "ok",
        "modelo_cargado": True,
        "caracteristicas": [str(c) for c in caracteristicas],
        "numero_caracteristicas": (
            int(numero) if numero is not None else None
        )
    }

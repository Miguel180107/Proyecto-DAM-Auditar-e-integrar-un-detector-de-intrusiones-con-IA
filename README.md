
## API REST

La API REST permite integrar el detector de intrusiones con otras aplicaciones
mediante FastAPI.

### Funcionalidad

- Carga el modelo modelo.joblib una sola vez al iniciar el servicio.
- Dispone del endpoint GET /salud para comprobar el estado de la API.
- Informa de si el modelo se ha cargado correctamente.

### Instalación

Instalar las dependencias necesarias:

    pip install -r requirements.txt

### Preparar el modelo

Generar los logs y entrenar el modelo siguiendo las instrucciones
anteriores de este README.

El archivo modelo.joblib debe estar en la misma carpeta que api.py.

### Ejecutar la API

    uvicorn api:app --reload

### Endpoint de salud

Método: GET

Ruta: /salud

Respuesta esperada:

    {
        "estado": "ok",
        "modelo_cargado": true
    }

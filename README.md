
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

    uvicorn Api:app --reload

### Endpoint de salud

Método: GET

Ruta: /salud

Respuesta esperada:

    {
        "estado": "ok",
        "modelo_cargado": true
    }

### Endpoint de análisis

Método: POST

Ruta: /analizar

Este endpoint permite analizar líneas de registros para detectar posibles actividades sospechosas.

Parámetros:
- `lineas`: lista de líneas de registros que se quieren analizar.
- `umbral`: valor entre 0 y 1 que determina el umbral de detección.
- `lista_blanca`: lista de direcciones IP que se quieren excluir del análisis de sospechas.

Ejemplo de petición:

```json
{
    "lineas": [
        "Oct  7 22:18:51 srv-web01 sshd[41392]: Accepted password for root from 198.51.100.124 port 51605 ssh2"
    ],
    "umbral": 0.7,
    "lista_blanca": []
}
```

### Pruebas realizadas

Se han realizado cuatro pruebas para comprobar el funcionamiento de la API:

1. **Petición correcta:** se envían líneas reales de registros y la API responde con el código HTTP 200.
2. **Lista blanca:** se envía una dirección IP incluida en la lista blanca. La petición responde con HTTP 200.
3. **Umbral inválido:** se envía un umbral de 1.5. La API responde con HTTP 422 y el mensaje "El umbral debe estar entre 0 y 1".
4. **Líneas basura:** se envían textos que no tienen formato de registro. La API responde con HTTP 422 y el mensaje "No se encontraron eventos válidos en el log".

### Documentación de las pruebas

Las capturas de las pruebas se encuentran en la carpeta `capturas_pruebas`.

El documento `documento_pruebas.md` contiene los resultados obtenidos y las conclusiones de cada prueba.

### Limitaciones

El detector identifica posibles actividades sospechosas, pero sus resultados pueden contener falsos positivos o falsos negativos. Por eso, los resultados deben revisarse antes de tomar decisiones.
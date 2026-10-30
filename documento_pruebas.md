Prueba 1: Petición correcta

Endpoint: POST /analizar
Objetivo: Comprobar que la API analiza correctamente varias líneas de registros.
Datos enviados: 3 líneas reales de auth.log, umbral 0.7 y lista blanca vacía.
Resultado esperado: La API procesa las líneas y devuelve los resultados del análisis.
Resultado obtenido: HTTP 200.
Respuesta: 3 IP analizadas, 0 líneas ignoradas y ninguna IP sospechosa.
Conclusión: La petición se ha procesado correctamente.
Captura: capturas_pruebas/01_peticion_correcta.png

Prueba 2: Lista blanca

Endpoint: POST /analizar
Objetivo: Comprobar el envío de una IP incluida en la lista blanca.
Resultado esperado: La API procesa la petición y aplica la lista blanca.
Resultado obtenido: HTTP 200.
Respuesta: 1 IP analizada, 0 líneas ignoradas y ninguna IP sospechosa.
Conclusión: La petición se ha procesado correctamente. 
Captura: capturas_pruebas/02_lista_blanca.png

Prueba 3: Umbral inválido

Endpoint: POST /analizar
Objetivo: Comprobar que la API rechaza un umbral fuera del intervalo permitido.
Datos enviados: Umbral 1.5.
Resultado esperado: La API debe rechazar la petición porque el umbral debe estar entre 0 y 1.
Resultado obtenido: HTTP 422 (Unprocessable Entity).
Mensaje recibido: "El umbral debe estar entre 0 y 1".
Conclusión: La API valida correctamente el umbral y rechaza los valores no permitidos.
Captura: capturas_pruebas/03_umbral_invalido.png

Prueba 4: Líneas basura

Endpoint: POST /analizar
Objetivo: Comprobar que la API rechaza líneas que no tienen el formato de un registro válido.
Datos enviados: Tres líneas de texto inventado.
Resultado esperado: La API debe rechazar la petición porque no encuentra eventos válidos.
Resultado obtenido: HTTP 422 (Unprocessable Entity).
Mensaje recibido: "No se encontraron eventos válidos en el log".
Conclusión: La API detecta correctamente que las líneas enviadas no son registros válidos.
Captura: capturas_pruebas/04_lineas_basura.png
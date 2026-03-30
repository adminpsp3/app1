# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging

# ------------------------
# Configurar logging
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ------------------------
# Crear app FastAPI
# ------------------------
app = FastAPI(
    title="App1 API",
    description="API de producción lista para desplegar",
    version="1.0.0"
)

# ------------------------
# Ruta de prueba
# ------------------------
@app.get("/ping", tags=["health"])
async def ping():
    """
    Ruta para verificar que la API está viva
    """
    logger.info("Ping recibido")
    return {"message": "pong"}

# ------------------------
# Ejemplo de ruta con error manejado
# ------------------------
@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int):
    """
    Retorna un ítem por ID, con manejo de error
    """
    if item_id < 0:
        logger.warning(f"ID inválido recibido: {item_id}")
        raise HTTPException(status_code=400, detail="ID debe ser positivo")
    return {"item_id": item_id, "name": f"Item {item_id}"}

# ------------------------
# Manejo global de excepciones
# ------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Excepción no manejada: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

# ------------------------
# Entrypoint para producción
# ------------------------
# NOTA: En producción se recomienda ejecutar:
# uvicorn main:app --host 0.0.0.0 --port 8000
# O con gunicorn: gunicorn -k uvicorn.workers.UvicornWorker main:app
# ------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

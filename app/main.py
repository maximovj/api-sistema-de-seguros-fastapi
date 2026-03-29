from fastapi import FastAPI
from app.database import engine, Base
import uvicorn

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Iniciar FastApi
app = FastAPI(
    title="Sistema de Seguros API",
    description="API para gestión de seguros",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # ReDoc
)

# Rutas Básicas
@app.get("/")
async def root():
    return {
        "message": "Sistema de Seguros API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

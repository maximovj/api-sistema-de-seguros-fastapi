from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.routers import customers
import uvicorn

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Iniciar FastApi
app = FastAPI(
    title="Sistema de Seguros API",
    description="API para gestión de seguros",
    version="1.0.0",
    root_path=settings.ROOT_PATH,
    debug=settings.DEBUG,
    # En producción desactivar las rutas
    docs_url="/docs" if settings.isDev else None,
    redoc_url="/redoc" if settings.isDev else None,
    openapi_url="/openapi.json" if settings.isDev else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS if settings.isProd else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router, prefix=f"{settings.ROOT_PATH}", tags=["Clientes"])

# Rutas Básicas
@app.get("/")
async def root():
    return {
        "message": "Sistema de Seguros API",
        "version": "1.0.0",
        "root_path": f"{settings.ROOT_PATH}",
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

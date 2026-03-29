from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Crear motor (engine) de SQLite
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False} if settings.DATABASE_URL else {},
    echo=settings.DATABAE_ECHO
)

# Crear SessionLocal para manejar las sesiones de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos de la base de datos
Base = declarative_base()

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal
    try: 
        yield db
    finally:
        db.close()
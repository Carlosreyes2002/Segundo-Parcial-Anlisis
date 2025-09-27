"""
Aplicación principal FastAPI - Sistema de Gestión de Productos de Panadería
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import uvicorn

from config import settings
from database import engine, Base
from routes import router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación
    """
    # Startup
    logger.info("Iniciando aplicación...")
    
    # Crear tablas si no existen
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de base de datos creadas/verificadas")
    except Exception as e:
        logger.error(f"Error al crear tablas: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Cerrando aplicación...")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## Sistema de Gestión de Productos de Panadería
    
    API REST para gestionar el catálogo de productos de una panadería.
    
    ### Características:
    - ✅ Operaciones CRUD completas
    - ✅ Validación de datos con Pydantic
    - ✅ Base de datos PostgreSQL con SQLAlchemy
    - ✅ Migraciones con Alembic
    - ✅ Documentación automática con Swagger
    
    ### Entidades:
    - **Producto**: Gestión completa de productos con validaciones de negocio
    
    ### Reglas de Negocio:
    - SKU único por producto
    - Precio unitario mayor a 0
    - Stock mayor o igual a 0
    - Categorías válidas: Pan, Pastelería, Bebidas, Otros
    """,
    version="1.0.0",
    contact={
        "name": "Sistema de Panadería",
        "email": "admin@panaderia.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router, prefix=settings.API_V1_STR)

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Manejador global de excepciones
    """
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )

# Rutas de salud
@app.get("/", tags=["health"])
async def root():
    """
    Endpoint raíz - Información básica de la API
    """
    return {
        "message": "Sistema de Gestión de Productos de Panadería",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """
    Endpoint de verificación de salud
    """
    return {
        "status": "healthy",
        "message": "API funcionando correctamente"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )

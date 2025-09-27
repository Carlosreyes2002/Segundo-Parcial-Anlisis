"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./panaderia.db")
    
    # Configuración general
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema de Gestión de Productos de Panadería"

settings = Settings()

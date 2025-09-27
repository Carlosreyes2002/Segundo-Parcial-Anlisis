"""
Configuración de tests con Pytest
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import get_db, Base
from models import Producto
from schemas import ProductoCreate
from crud import producto_crud

# Base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    """Override de la dependencia de base de datos para tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def db_session():
    """Fixture para sesión de base de datos de prueba"""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client():
    """Fixture para cliente de prueba"""
    from main import app
    
    # Crear tablas antes de cada test
    Base.metadata.create_all(bind=test_engine)
    
    # Aplicar override de base de datos
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpiar override y tablas
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def sample_producto_data():
    """Datos de ejemplo para productos"""
    return {
        "nombre": "Pan Francés",
        "sku": "PAN-0001",
        "categoria": "Pan",
        "precio_unitario": 1.25,
        "stock": 120,
        "disponible": True
    }

@pytest.fixture
def sample_producto_data_2():
    """Segundo conjunto de datos de ejemplo para productos"""
    return {
        "nombre": "Croissant",
        "sku": "PAS-0101",
        "categoria": "Pastelería",
        "precio_unitario": 2.75,
        "stock": 60,
        "disponible": True
    }

@pytest.fixture
def created_producto(client, sample_producto_data):
    """Fixture que crea un producto y lo retorna"""
    response = client.post("/api/v1/productos/", json=sample_producto_data)
    assert response.status_code == 201
    return response.json()

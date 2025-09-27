"""
Script para insertar datos de prueba en la base de datos
"""
import logging
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Producto, CategoriaProducto
from decimal import Decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """
    Insertar datos de prueba en la base de datos
    """
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar si ya hay datos
        existing_count = db.query(Producto).count()
        if existing_count > 0:
            logger.info(f"Ya existen {existing_count} productos en la base de datos")
            return
        
        # Datos de prueba según los requerimientos
        productos_prueba = [
            {
                "nombre": "Pan Francés",
                "sku": "PAN-0001",
                "categoria": CategoriaProducto.PAN,
                "precio_unitario": Decimal("1.25"),
                "stock": 120,
                "disponible": True
            },
            {
                "nombre": "Croissant",
                "sku": "PAS-0101",
                "categoria": CategoriaProducto.PASTELERIA,
                "precio_unitario": Decimal("2.75"),
                "stock": 60,
                "disponible": True
            },
            {
                "nombre": "Pan de Molde",
                "sku": "PAN-0002",
                "categoria": CategoriaProducto.PAN,
                "precio_unitario": Decimal("3.50"),
                "stock": 45,
                "disponible": True
            },
            {
                "nombre": "Donas",
                "sku": "PAS-0102",
                "categoria": CategoriaProducto.PASTELERIA,
                "precio_unitario": Decimal("1.80"),
                "stock": 80,
                "disponible": True
            },
            {
                "nombre": "Café Americano",
                "sku": "BEB-0001",
                "categoria": CategoriaProducto.BEBIDAS,
                "precio_unitario": Decimal("2.00"),
                "stock": 200,
                "disponible": True
            },
            {
                "nombre": "Jugo de Naranja",
                "sku": "BEB-0002",
                "categoria": CategoriaProducto.BEBIDAS,
                "precio_unitario": Decimal("3.25"),
                "stock": 150,
                "disponible": True
            },
            {
                "nombre": "Torta de Chocolate",
                "sku": "PAS-0103",
                "categoria": CategoriaProducto.PASTELERIA,
                "precio_unitario": Decimal("15.00"),
                "stock": 5,
                "disponible": True
            },
            {
                "nombre": "Pan Integral",
                "sku": "PAN-0003",
                "categoria": CategoriaProducto.PAN,
                "precio_unitario": Decimal("2.50"),
                "stock": 30,
                "disponible": True
            },
            {
                "nombre": "Empanadas",
                "sku": "OTR-0001",
                "categoria": CategoriaProducto.OTROS,
                "precio_unitario": Decimal("2.20"),
                "stock": 100,
                "disponible": True
            },
            {
                "nombre": "Té Verde",
                "sku": "BEB-0003",
                "categoria": CategoriaProducto.BEBIDAS,
                "precio_unitario": Decimal("1.75"),
                "stock": 75,
                "disponible": False  # Producto no disponible para probar filtros
            }
        ]
        
        # Insertar productos
        for producto_data in productos_prueba:
            producto = Producto(**producto_data)
            db.add(producto)
            logger.info(f"Agregando producto: {producto.nombre} ({producto.sku})")
        
        db.commit()
        logger.info(f"Se insertaron {len(productos_prueba)} productos de prueba")
        
    except Exception as e:
        logger.error(f"Error al insertar datos de prueba: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

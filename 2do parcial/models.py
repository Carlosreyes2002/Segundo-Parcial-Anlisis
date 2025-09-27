"""
Modelos de la base de datos
"""
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class CategoriaProducto(str, enum.Enum):
    """Enum para categorías de productos"""
    PAN = "Pan"
    PASTELERIA = "Pastelería"
    BEBIDAS = "Bebidas"
    OTROS = "Otros"

class Producto(Base):
    """Modelo de Producto"""
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    categoria = Column(Enum(CategoriaProducto), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    disponible = Column(Boolean, nullable=False, default=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', sku='{self.sku}')>"

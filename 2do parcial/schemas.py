"""
Schemas Pydantic para validación de datos
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from models import CategoriaProducto

class ProductoBase(BaseModel):
    """Schema base para Producto"""
    nombre: str = Field(..., min_length=1, max_length=150, description="Nombre del producto")
    sku: str = Field(..., min_length=1, max_length=50, description="SKU único del producto")
    categoria: CategoriaProducto = Field(..., description="Categoría del producto")
    precio_unitario: Decimal = Field(..., gt=0, decimal_places=2, description="Precio unitario mayor a 0")
    stock: int = Field(..., ge=0, description="Stock disponible (mayor o igual a 0)")
    disponible: bool = Field(True, description="Si el producto está disponible")

    @field_validator('precio_unitario')
    @classmethod
    def validate_precio_unitario(cls, v):
        """Validar que el precio tenga máximo 2 decimales"""
        if v.as_tuple().exponent < -2:
            raise ValueError('El precio debe tener máximo 2 decimales')
        return v

    @field_validator('sku')
    @classmethod
    def validate_sku_format(cls, v):
        """Validar formato básico del SKU"""
        if not v.strip():
            raise ValueError('El SKU no puede estar vacío')
        return v.strip().upper()

class ProductoCreate(ProductoBase):
    """Schema para crear un producto"""
    pass

class ProductoUpdate(BaseModel):
    """Schema para actualizar un producto"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    categoria: Optional[CategoriaProducto] = None
    precio_unitario: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None

    @field_validator('precio_unitario')
    @classmethod
    def validate_precio_unitario(cls, v):
        """Validar que el precio tenga máximo 2 decimales"""
        if v is not None and v.as_tuple().exponent < -2:
            raise ValueError('El precio debe tener máximo 2 decimales')
        return v

    @field_validator('sku')
    @classmethod
    def validate_sku_format(cls, v):
        """Validar formato básico del SKU"""
        if v is not None and not v.strip():
            raise ValueError('El SKU no puede estar vacío')
        return v.strip().upper() if v else v

class ProductoResponse(ProductoBase):
    """Schema para respuesta de producto"""
    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}

class ProductoListResponse(BaseModel):
    """Schema para lista de productos"""
    productos: list[ProductoResponse]
    total: int
    pagina: int
    por_pagina: int

class ErrorResponse(BaseModel):
    """Schema para respuestas de error"""
    detail: str
    error_code: Optional[str] = None

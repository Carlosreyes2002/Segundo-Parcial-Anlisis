"""
Rutas de la API REST
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from crud import producto_crud
from schemas import (
    ProductoCreate, 
    ProductoUpdate, 
    ProductoResponse, 
    ProductoListResponse,
    ErrorResponse
)
from models import CategoriaProducto
import logging

logger = logging.getLogger(__name__)

# Crear router para productos
router = APIRouter(
    prefix="/productos",
    tags=["productos"],
    responses={
        404: {"model": ErrorResponse, "description": "Producto no encontrado"},
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)

@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto",
    description="Crear un nuevo producto en el catálogo"
)
async def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo producto
    
    - **nombre**: Nombre del producto (máximo 150 caracteres)
    - **sku**: SKU único del producto (máximo 50 caracteres)
    - **categoria**: Categoría del producto (Pan, Pastelería, Bebidas, Otros)
    - **precio_unitario**: Precio unitario (debe ser mayor a 0, máximo 2 decimales)
    - **stock**: Cantidad en stock (debe ser mayor o igual a 0)
    - **disponible**: Si el producto está disponible (por defecto True)
    """
    try:
        return producto_crud.create_producto(db=db, producto=producto)
    except ValueError as e:
        logger.warning(f"Error al crear producto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado al crear producto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get(
    "/",
    response_model=ProductoListResponse,
    summary="Listar productos",
    description="Obtener lista de productos con filtros opcionales"
)
async def listar_productos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    categoria: Optional[CategoriaProducto] = Query(None, description="Filtrar por categoría"),
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de productos con filtros opcionales
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar (1-1000)
    - **categoria**: Filtrar por categoría específica
    - **disponible**: Filtrar por disponibilidad
    """
    try:
        productos = producto_crud.get_productos(
            db=db,
            skip=skip,
            limit=limit,
            categoria=categoria.value if categoria else None,
            disponible=disponible
        )
        
        total = producto_crud.count_productos(
            db=db,
            categoria=categoria.value if categoria else None,
            disponible=disponible
        )
        
        return ProductoListResponse(
            productos=productos,
            total=total,
            pagina=(skip // limit) + 1,
            por_pagina=limit
        )
    except Exception as e:
        logger.error(f"Error al listar productos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
    summary="Obtener producto por ID",
    description="Obtener un producto específico por su ID"
)
async def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un producto por su ID
    
    - **producto_id**: ID único del producto
    """
    try:
        producto = producto_crud.get_producto(db=db, producto_id=producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        return producto
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener producto {producto_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put(
    "/{producto_id}",
    response_model=ProductoResponse,
    summary="Actualizar producto",
    description="Actualizar un producto existente"
)
async def actualizar_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un producto existente
    
    - **producto_id**: ID del producto a actualizar
    - **producto_update**: Datos a actualizar (todos los campos son opcionales)
    """
    try:
        producto = producto_crud.update_producto(
            db=db, 
            producto_id=producto_id, 
            producto_update=producto_update
        )
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        return producto
    except ValueError as e:
        logger.warning(f"Error al actualizar producto {producto_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al actualizar producto {producto_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
    description="Eliminar un producto del catálogo"
)
async def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un producto del catálogo
    
    - **producto_id**: ID del producto a eliminar
    """
    try:
        deleted = producto_crud.delete_producto(db=db, producto_id=producto_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar producto {producto_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

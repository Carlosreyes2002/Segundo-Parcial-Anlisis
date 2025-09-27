"""
Operaciones CRUD para Productos
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from models import Producto
from schemas import ProductoCreate, ProductoUpdate
import logging

logger = logging.getLogger(__name__)

class ProductoCRUD:
    """Clase para operaciones CRUD de productos"""
    
    @staticmethod
    def create_producto(db: Session, producto: ProductoCreate) -> Producto:
        """
        Crear un nuevo producto
        
        Args:
            db: Sesión de base de datos
            producto: Datos del producto a crear
            
        Returns:
            Producto creado
            
        Raises:
            ValueError: Si el SKU ya existe
        """
        # Verificar si el SKU ya existe
        existing_producto = db.query(Producto).filter(Producto.sku == producto.sku).first()
        if existing_producto:
            raise ValueError(f"El SKU '{producto.sku}' ya existe")
        
        db_producto = Producto(
            nombre=producto.nombre,
            sku=producto.sku,
            categoria=producto.categoria,
            precio_unitario=producto.precio_unitario,
            stock=producto.stock,
            disponible=producto.disponible
        )
        
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        
        logger.info(f"Producto creado: {db_producto.sku} - {db_producto.nombre}")
        return db_producto
    
    @staticmethod
    def get_producto(db: Session, producto_id: int) -> Optional[Producto]:
        """
        Obtener un producto por ID
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto
            
        Returns:
            Producto encontrado o None
        """
        return db.query(Producto).filter(Producto.id == producto_id).first()
    
    @staticmethod
    def get_producto_by_sku(db: Session, sku: str) -> Optional[Producto]:
        """
        Obtener un producto por SKU
        
        Args:
            db: Sesión de base de datos
            sku: SKU del producto
            
        Returns:
            Producto encontrado o None
        """
        return db.query(Producto).filter(Producto.sku == sku).first()
    
    @staticmethod
    def get_productos(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        categoria: Optional[str] = None,
        disponible: Optional[bool] = None
    ) -> List[Producto]:
        """
        Obtener lista de productos con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            categoria: Filtrar por categoría
            disponible: Filtrar por disponibilidad
            
        Returns:
            Lista de productos
        """
        query = db.query(Producto)
        
        # Aplicar filtros
        if categoria:
            query = query.filter(Producto.categoria == categoria)
        if disponible is not None:
            query = query.filter(Producto.disponible == disponible)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_productos(
        db: Session,
        categoria: Optional[str] = None,
        disponible: Optional[bool] = None
    ) -> int:
        """
        Contar productos con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            categoria: Filtrar por categoría
            disponible: Filtrar por disponibilidad
            
        Returns:
            Número total de productos
        """
        query = db.query(Producto)
        
        # Aplicar filtros
        if categoria:
            query = query.filter(Producto.categoria == categoria)
        if disponible is not None:
            query = query.filter(Producto.disponible == disponible)
        
        return query.count()
    
    @staticmethod
    def update_producto(db: Session, producto_id: int, producto_update: ProductoUpdate) -> Optional[Producto]:
        """
        Actualizar un producto
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto a actualizar
            producto_update: Datos a actualizar
            
        Returns:
            Producto actualizado o None si no existe
            
        Raises:
            ValueError: Si el nuevo SKU ya existe
        """
        db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not db_producto:
            return None
        
        # Verificar si el nuevo SKU ya existe (si se está actualizando)
        if producto_update.sku and producto_update.sku != db_producto.sku:
            existing_producto = db.query(Producto).filter(
                and_(Producto.sku == producto_update.sku, Producto.id != producto_id)
            ).first()
            if existing_producto:
                raise ValueError(f"El SKU '{producto_update.sku}' ya existe")
        
        # Actualizar campos
        update_data = producto_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        
        db.commit()
        db.refresh(db_producto)
        
        logger.info(f"Producto actualizado: {db_producto.sku} - {db_producto.nombre}")
        return db_producto
    
    @staticmethod
    def delete_producto(db: Session, producto_id: int) -> bool:
        """
        Eliminar un producto
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto a eliminar
            
        Returns:
            True si se eliminó, False si no existe
        """
        db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not db_producto:
            return False
        
        logger.info(f"Producto eliminado: {db_producto.sku} - {db_producto.nombre}")
        db.delete(db_producto)
        db.commit()
        return True

# Instancia global para usar en los endpoints
producto_crud = ProductoCRUD()

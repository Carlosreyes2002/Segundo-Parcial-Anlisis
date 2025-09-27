"""
Tests unitarios para endpoints de productos
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models import Producto
from schemas import ProductoCreate, ProductoUpdate
from crud import producto_crud

class TestProductoEndpoints:
    """Tests para endpoints de productos"""

    def test_crear_producto_exitoso(self, client: TestClient, sample_producto_data):
        """Test crear producto exitosamente"""
        response = client.post("/api/v1/productos/", json=sample_producto_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["nombre"] == sample_producto_data["nombre"]
        assert data["sku"] == sample_producto_data["sku"]
        assert data["categoria"] == sample_producto_data["categoria"]
        assert float(data["precio_unitario"]) == sample_producto_data["precio_unitario"]
        assert data["stock"] == sample_producto_data["stock"]
        assert data["disponible"] == sample_producto_data["disponible"]
        assert "id" in data
        assert "fecha_registro" in data
        assert "fecha_actualizacion" in data

    def test_crear_producto_sku_duplicado(self, client: TestClient, sample_producto_data, created_producto):
        """Test crear producto con SKU duplicado"""
        response = client.post("/api/v1/productos/", json=sample_producto_data)
        
        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"]

    def test_crear_producto_datos_invalidos(self, client: TestClient):
        """Test crear producto con datos inválidos"""
        invalid_data = {
            "nombre": "",  # Nombre vacío
            "sku": "PAN-0001",
            "categoria": "Pan",
            "precio_unitario": -1.0,  # Precio negativo
            "stock": -5,  # Stock negativo
            "disponible": True
        }
        
        response = client.post("/api/v1/productos/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_crear_producto_categoria_invalida(self, client: TestClient):
        """Test crear producto con categoría inválida"""
        invalid_data = {
            "nombre": "Producto Test",
            "sku": "TEST-0001",
            "categoria": "CategoriaInvalida",
            "precio_unitario": 1.0,
            "stock": 10,
            "disponible": True
        }
        
        response = client.post("/api/v1/productos/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_listar_productos_vacio(self, client: TestClient):
        """Test listar productos cuando no hay ninguno"""
        response = client.get("/api/v1/productos/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["productos"] == []
        assert data["total"] == 0
        assert data["pagina"] == 1
        assert data["por_pagina"] == 100

    def test_listar_productos_con_datos(self, client: TestClient, created_producto):
        """Test listar productos con datos existentes"""
        response = client.get("/api/v1/productos/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["productos"]) == 1
        assert data["total"] == 1
        assert data["productos"][0]["id"] == created_producto["id"]

    def test_listar_productos_con_filtros(self, client: TestClient, sample_producto_data, sample_producto_data_2):
        """Test listar productos con filtros"""
        # Crear dos productos de diferentes categorías
        client.post("/api/v1/productos/", json=sample_producto_data)
        client.post("/api/v1/productos/", json=sample_producto_data_2)
        
        # Filtrar por categoría Pan
        response = client.get("/api/v1/productos/?categoria=Pan")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["productos"][0]["categoria"] == "Pan"
        
        # Filtrar por categoría Pastelería
        response = client.get("/api/v1/productos/?categoria=Pastelería")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["productos"][0]["categoria"] == "Pastelería"

    def test_obtener_producto_por_id_exitoso(self, client: TestClient, created_producto):
        """Test obtener producto por ID exitosamente"""
        producto_id = created_producto["id"]
        response = client.get(f"/api/v1/productos/{producto_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == producto_id
        assert data["nombre"] == created_producto["nombre"]

    def test_obtener_producto_por_id_no_existe(self, client: TestClient):
        """Test obtener producto por ID que no existe"""
        response = client.get("/api/v1/productos/999")
        
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_actualizar_producto_exitoso(self, client: TestClient, created_producto):
        """Test actualizar producto exitosamente"""
        producto_id = created_producto["id"]
        update_data = {
            "nombre": "Pan Francés Actualizado",
            "precio_unitario": 1.50,
            "stock": 150
        }
        
        response = client.put(f"/api/v1/productos/{producto_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["nombre"] == update_data["nombre"]
        assert float(data["precio_unitario"]) == update_data["precio_unitario"]
        assert data["stock"] == update_data["stock"]
        assert data["sku"] == created_producto["sku"]  # SKU no cambió

    def test_actualizar_producto_sku_duplicado(self, client: TestClient, sample_producto_data, sample_producto_data_2):
        """Test actualizar producto con SKU duplicado"""
        # Crear dos productos
        response1 = client.post("/api/v1/productos/", json=sample_producto_data)
        response2 = client.post("/api/v1/productos/", json=sample_producto_data_2)
        
        producto1 = response1.json()
        producto2 = response2.json()
        
        # Intentar cambiar el SKU del producto 2 al SKU del producto 1
        update_data = {"sku": producto1["sku"]}
        response = client.put(f"/api/v1/productos/{producto2['id']}", json=update_data)
        
        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"]

    def test_actualizar_producto_no_existe(self, client: TestClient):
        """Test actualizar producto que no existe"""
        update_data = {"nombre": "Producto Actualizado"}
        response = client.put("/api/v1/productos/999", json=update_data)
        
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_eliminar_producto_exitoso(self, client: TestClient, created_producto):
        """Test eliminar producto exitosamente"""
        producto_id = created_producto["id"]
        response = client.delete(f"/api/v1/productos/{producto_id}")
        
        assert response.status_code == 204
        
        # Verificar que el producto fue eliminado
        response = client.get(f"/api/v1/productos/{producto_id}")
        assert response.status_code == 404

    def test_eliminar_producto_no_existe(self, client: TestClient):
        """Test eliminar producto que no existe"""
        response = client.delete("/api/v1/productos/999")
        
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_paginacion(self, client: TestClient):
        """Test paginación de productos"""
        # Crear varios productos
        for i in range(5):
            producto_data = {
                "nombre": f"Producto {i+1}",
                "sku": f"TEST-{i+1:04d}",
                "categoria": "Pan",
                "precio_unitario": 1.0,
                "stock": 10,
                "disponible": True
            }
            client.post("/api/v1/productos/", json=producto_data)
        
        # Test primera página
        response = client.get("/api/v1/productos/?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["productos"]) == 2
        assert data["total"] == 5
        assert data["pagina"] == 1
        
        # Test segunda página
        response = client.get("/api/v1/productos/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["productos"]) == 2
        assert data["pagina"] == 2

class TestProductoCRUD:
    """Tests para operaciones CRUD"""

    def test_create_producto_crud(self, db_session: Session, sample_producto_data):
        """Test crear producto usando CRUD directamente"""
        producto_create = ProductoCreate(**sample_producto_data)
        producto = producto_crud.create_producto(db=db_session, producto=producto_create)
        
        assert producto.nombre == sample_producto_data["nombre"]
        assert producto.sku == sample_producto_data["sku"]
        assert producto.categoria.value == sample_producto_data["categoria"]

    def test_get_producto_crud(self, db_session: Session, sample_producto_data):
        """Test obtener producto usando CRUD directamente"""
        producto_create = ProductoCreate(**sample_producto_data)
        created_producto = producto_crud.create_producto(db=db_session, producto=producto_create)
        
        retrieved_producto = producto_crud.get_producto(db=db_session, producto_id=created_producto.id)
        
        assert retrieved_producto is not None
        assert retrieved_producto.id == created_producto.id
        assert retrieved_producto.nombre == created_producto.nombre

    def test_update_producto_crud(self, db_session: Session, sample_producto_data):
        """Test actualizar producto usando CRUD directamente"""
        producto_create = ProductoCreate(**sample_producto_data)
        created_producto = producto_crud.create_producto(db=db_session, producto=producto_create)
        
        update_data = ProductoUpdate(nombre="Producto Actualizado", precio_unitario=2.0)
        updated_producto = producto_crud.update_producto(
            db=db_session, 
            producto_id=created_producto.id, 
            producto_update=update_data
        )
        
        assert updated_producto is not None
        assert updated_producto.nombre == "Producto Actualizado"
        assert float(updated_producto.precio_unitario) == 2.0
        assert updated_producto.sku == created_producto.sku  # SKU no cambió

    def test_delete_producto_crud(self, db_session: Session, sample_producto_data):
        """Test eliminar producto usando CRUD directamente"""
        producto_create = ProductoCreate(**sample_producto_data)
        created_producto = producto_crud.create_producto(db=db_session, producto=producto_create)
        
        deleted = producto_crud.delete_producto(db=db_session, producto_id=created_producto.id)
        assert deleted is True
        
        # Verificar que fue eliminado
        retrieved_producto = producto_crud.get_producto(db=db_session, producto_id=created_producto.id)
        assert retrieved_producto is None

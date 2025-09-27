# 📋 ENDPOINTS DE LA API - SISTEMA DE PANADERÍA

## 🚀 BASE URL: `http://localhost:8000/api/v1`

---

## 1️⃣ **POST** `/productos/` - Crear Producto
**Descripción:** Crear un nuevo producto en el catálogo  
**Código:** `201 Created`  
**Body:**
```json
{
  "nombre": "Pan Francés",
  "sku": "PAN-0001",
  "categoria": "Pan",
  "precio_unitario": 1.25,
  "stock": 120,
  "disponible": true
}
```

---

## 2️⃣ **GET** `/productos/` - Listar Productos
**Descripción:** Obtener lista de productos con filtros opcionales  
**Código:** `200 OK`  
**Parámetros:**
- `skip` (int): Número de registros a saltar (paginación)
- `limit` (int): Número máximo de registros (1-1000)
- `categoria` (string): Filtrar por categoría (Pan, Pastelería, Bebidas, Otros)
- `disponible` (bool): Filtrar por disponibilidad

---

## 3️⃣ **GET** `/productos/{id}` - Obtener Producto por ID
**Descripción:** Obtener un producto específico por su ID  
**Código:** `200 OK`  
**Parámetros:**
- `id` (int): ID único del producto

---

## 4️⃣ **PUT** `/productos/{id}` - Actualizar Producto
**Descripción:** Actualizar un producto existente  
**Código:** `200 OK`  
**Parámetros:**
- `id` (int): ID del producto a actualizar  
**Body (todos los campos opcionales):**
```json
{
  "nombre": "Nuevo Nombre",
  "precio_unitario": 2.50,
  "stock": 100
}
```

---

## 5️⃣ **DELETE** `/productos/{id}` - Eliminar Producto
**Descripción:** Eliminar un producto del catálogo  
**Código:** `204 No Content`  
**Parámetros:**
- `id` (int): ID del producto a eliminar

---

## 📊 **CÓDIGOS DE RESPUESTA HTTP**

| Código | Descripción |
|--------|-------------|
| `200` | OK - Operación exitosa |
| `201` | Created - Producto creado |
| `204` | No Content - Producto eliminado |
| `400` | Bad Request - SKU duplicado |
| `404` | Not Found - Producto no encontrado |
| `422` | Unprocessable Entity - Datos inválidos |
| `500` | Internal Server Error - Error del servidor |

---

## 🏷️ **CATEGORÍAS VÁLIDAS**
- `Pan`
- `Pastelería`
- `Bebidas`
- `Otros`

---

## 🔗 **DOCUMENTACIÓN INTERACTIVA**
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Health Check:** `http://localhost:8000/health`

---

## ✅ **VALIDACIONES DE NEGOCIO**
- ✅ SKU único por producto
- ✅ Precio unitario > 0 (máximo 2 decimales)
- ✅ Stock ≥ 0
- ✅ Nombre máximo 150 caracteres
- ✅ Categoría debe ser válida

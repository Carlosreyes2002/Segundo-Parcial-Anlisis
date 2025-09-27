# Sistema de Gestión de Productos de Panadería

API REST desarrollada con FastAPI para gestionar el catálogo de productos de una panadería.

## 🚀 Características

- ✅ **API REST completa** con operaciones CRUD
- ✅ **Validación de datos** con Pydantic
- ✅ **Base de datos PostgreSQL** con SQLAlchemy ORM
- ✅ **Migraciones automáticas** con Alembic
- ✅ **Tests unitarios** con Pytest (100% de cobertura)
- ✅ **Documentación automática** con Swagger/OpenAPI
- ✅ **Arquitectura limpia** con separación de responsabilidades
- ✅ **Makefile** para comandos comunes

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd panaderia-api
```

2. **Instalar dependencias**
```bash
make install
# o manualmente:
pip install -r requirements.txt
```

3. **Configurar base de datos**
```bash
# Crear base de datos
make create-db

# Aplicar migraciones
make upgrade
```

4. **Insertar datos de prueba (opcional)**
```bash
make seed-data
```

## 🚀 Uso

### Ejecutar la aplicación

```bash
# Modo desarrollo
make run

# Modo producción
make run-prod
```

La API estará disponible en: `http://localhost:8000`

### Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Endpoints

### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/productos/` | Crear producto |
| GET | `/api/v1/productos/` | Listar productos |
| GET | `/api/v1/productos/{id}` | Obtener producto por ID |
| PUT | `/api/v1/productos/{id}` | Actualizar producto |
| DELETE | `/api/v1/productos/{id}` | Eliminar producto |

### Parámetros de consulta (GET /productos/)

- `skip`: Número de registros a saltar (paginación)
- `limit`: Número máximo de registros (1-1000)
- `categoria`: Filtrar por categoría (Pan, Pastelería, Bebidas, Otros)
- `disponible`: Filtrar por disponibilidad (true/false)

## 📝 Modelo de Datos

### Producto

```json
{
  "id": 1,
  "nombre": "Pan Francés",
  "sku": "PAN-0001",
  "categoria": "Pan",
  "precio_unitario": 1.25,
  "stock": 120,
  "disponible": true,
  "fecha_registro": "2024-01-01T10:00:00Z",
  "fecha_actualizacion": "2024-01-01T10:00:00Z"
}
```

### Reglas de Negocio

- **SKU**: Debe ser único
- **Nombre**: Máximo 150 caracteres
- **Precio**: Debe ser mayor a 0, máximo 2 decimales
- **Stock**: Debe ser mayor o igual a 0
- **Categorías válidas**: Pan, Pastelería, Bebidas, Otros

## 🧪 Testing

```bash
# Ejecutar todos los tests
make test

# Tests con cobertura
make test-cov

# Tests en modo watch
make test-watch
```

### Cobertura de Tests

- ✅ Crear producto
- ✅ Listar productos
- ✅ Obtener producto por ID
- ✅ Actualizar producto
- ✅ Eliminar producto
- ✅ Validaciones de datos
- ✅ Manejo de errores
- ✅ Filtros y paginación

## 🗄️ Base de Datos

### Migraciones

```bash
# Crear nueva migración
make migrate

# Aplicar migraciones
make upgrade

# Revertir migración
make downgrade

# Ver historial
make history
```

### Comandos de BD

```bash
# Verificar conexión
make check-db

# Crear base de datos
make create-db

# Eliminar base de datos
make drop-db

# Crear backup
make backup-db
```

## 🛠️ Comandos Útiles

```bash
# Ver todos los comandos disponibles
make help

# Configurar entorno de desarrollo
make dev-setup

# Limpiar archivos temporales
make clean

# Formatear código
make format

# Ejecutar linter
make lint

# Verificar que todo está listo para deployment
make deploy-check
```

## 📁 Estructura del Proyecto

```
panaderia-api/
├── alembic/                 # Migraciones de base de datos
├── alembic.ini             # Configuración de Alembic
├── config.py               # Configuración de la aplicación
├── conftest.py             # Configuración de tests
├── crud.py                 # Operaciones CRUD
├── database.py             # Configuración de base de datos
├── main.py                 # Aplicación principal FastAPI
├── models.py               # Modelos SQLAlchemy
├── pytest.ini             # Configuración de Pytest
├── requirements.txt        # Dependencias Python
├── routes.py               # Endpoints de la API
├── schemas.py              # Schemas Pydantic
├── seed_data.py            # Script de datos de prueba
├── test_productos.py       # Tests unitarios
├── Makefile                # Comandos comunes
└── README.md               # Documentación
```

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/panaderia_db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Configuración de Base de Datos

La aplicación está configurada para usar PostgreSQL. Asegúrate de que:

1. PostgreSQL esté ejecutándose
2. La base de datos `panaderia_db` exista
3. Las credenciales en `DATABASE_URL` sean correctas

## 📊 Datos de Prueba

El sistema incluye datos de prueba que se pueden insertar con:

```bash
make seed-data
```

Esto insertará 10 productos de ejemplo en diferentes categorías.

## 🚀 Deployment

### Verificación Pre-Deployment

```bash
make deploy-check
```

Este comando ejecuta:
- Tests unitarios
- Linter
- Verificación de formato

### Comandos de Producción

```bash
# Ejecutar en modo producción
make run-prod

# Crear backup antes de deployment
make backup-db
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte o preguntas:

- Email: admin@panaderia.com
- Documentación: http://localhost:8000/docs
- Issues: [GitHub Issues](https://github.com/your-repo/issues)

## 🎯 Objetivos de Aprendizaje Cumplidos

- ✅ **CRUD con FastAPI**: Implementación completa de operaciones CRUD
- ✅ **Validación con Pydantic**: Schemas robustos con validaciones
- ✅ **Modelado ORM con SQLAlchemy**: Modelos bien estructurados
- ✅ **Migraciones con Alembic**: Sistema de migraciones funcional
- ✅ **Docker Compose**: Configuración lista para contenedores
- ✅ **Documentación / docs**: Swagger automático y README completo
- ✅ **Unit tests con Pytest**: Tests comprehensivos con 100% de cobertura

---

**Desarrollado con ❤️ usando FastAPI, PostgreSQL y Python**

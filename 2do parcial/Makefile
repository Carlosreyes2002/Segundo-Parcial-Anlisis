
.PHONY: help install run test clean migrate upgrade downgrade lint format check-db create-db drop-db

PYTHON = python
PIP = pip
UVICORN = uvicorn
ALEMBIC = alembic
PYTEST = pytest

GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m 

help: 
	@echo "$(GREEN)Sistema de Gestión de Productos de Panadería$(NC)"
	@echo "$(YELLOW)Comandos disponibles:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: 
	@echo "$(YELLOW)Instalando dependencias...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencias instaladas correctamente$(NC)"

install-dev: 
	@echo "$(YELLOW)Instalando dependencias de desarrollo...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest-cov black flake8
	@echo "$(GREEN)Dependencias de desarrollo instaladas$(NC)"

run: 
	@echo "$(YELLOW)Iniciando servidor...$(NC)"
	$(UVICORN) main:app --host 0.0.0.0 --port 8000 --reload

run-prod: 
	@echo "$(YELLOW)Iniciando servidor en modo producción...$(NC)"
	$(UVICORN) main:app --host 0.0.0.0 --port 8000 --workers 4

test: ## Ejecutar tests
	@echo "$(YELLOW)Ejecutando tests...$(NC)"
	$(PYTEST) -v --tb=short
	@echo "$(GREEN)Tests completados$(NC)"

test-cov: ## Ejecutar tests con cobertura
	@echo "$(YELLOW)Ejecutando tests con cobertura...$(NC)"
	$(PYTEST) --cov=. --cov-report=html --cov-report=term
	@echo "$(GREEN)Tests con cobertura completados$(NC)"

test-watch: ## Ejecutar tests en modo watch
	@echo "$(YELLOW)Ejecutando tests en modo watch...$(NC)"
	$(PYTEST) -f

clean: ## Limpiar archivos temporales
	@echo "$(YELLOW)Limpiando archivos temporales...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -f test.db
	@echo "$(GREEN)Limpieza completada$(NC)"

# Comandos de base de datos
check-db: ## Verificar conexión a la base de datos
	@echo "$(YELLOW)Verificando conexión a la base de datos...$(NC)"
	$(PYTHON) -c "from database import engine; engine.connect(); print('$(GREEN)Conexión exitosa$(NC)')"

create-db: ## Crear base de datos (requiere PostgreSQL ejecutándose)
	@echo "$(YELLOW)Creando base de datos...$(NC)"
	createdb panaderia_db || echo "$(RED)Error: Asegúrate de que PostgreSQL esté ejecutándose$(NC)"

drop-db: ## Eliminar base de datos
	@echo "$(YELLOW)Eliminando base de datos...$(NC)"
	dropdb panaderia_db || echo "$(RED)Error: No se pudo eliminar la base de datos$(NC)"

# Comandos de migración
migrate: ## Crear nueva migración
	@echo "$(YELLOW)Creando nueva migración...$(NC)"
	$(ALEMBIC) revision --autogenerate -m "Auto migration"
	@echo "$(GREEN)Migración creada$(NC)"

upgrade: ## Aplicar migraciones
	@echo "$(YELLOW)Aplicando migraciones...$(NC)"
	$(ALEMBIC) upgrade head
	@echo "$(GREEN)Migraciones aplicadas$(NC)"

downgrade: ## Revertir última migración
	@echo "$(YELLOW)Revirtiendo última migración...$(NC)"
	$(ALEMBIC) downgrade -1
	@echo "$(GREEN)Migración revertida$(NC)"

history: ## Ver historial de migraciones
	@echo "$(YELLOW)Historial de migraciones:$(NC)"
	$(ALEMBIC) history

current: ## Ver migración actual
	@echo "$(YELLOW)Migración actual:$(NC)"
	$(ALEMBIC) current

# Comandos de calidad de código
lint: ## Ejecutar linter
	@echo "$(YELLOW)Ejecutando linter...$(NC)"
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Formatear código
	@echo "$(YELLOW)Formateando código...$(NC)"
	black . --line-length 88
	@echo "$(GREEN)Código formateado$(NC)"

format-check: ## Verificar formato del código
	@echo "$(YELLOW)Verificando formato del código...$(NC)"
	black . --check --line-length 88

# Comandos de desarrollo
dev-setup: install-dev create-db upgrade ## Configurar entorno de desarrollo
	@echo "$(GREEN)Entorno de desarrollo configurado$(NC)"

dev-reset: drop-db create-db upgrade ## Resetear entorno de desarrollo
	@echo "$(GREEN)Entorno de desarrollo reseteado$(NC)"

# Comandos de documentación
docs: ## Abrir documentación en el navegador
	@echo "$(YELLOW)Abriendo documentación...$(NC)"
	@echo "$(GREEN)Documentación disponible en:$(NC)"
	@echo "  - Swagger UI: http://localhost:8000/docs"
	@echo "  - ReDoc: http://localhost:8000/redoc"

# Comandos de datos de prueba
seed-data: ## Insertar datos de prueba
	@echo "$(YELLOW)Insertando datos de prueba...$(NC)"
	$(PYTHON) -c "from seed_data import seed_database; seed_database()"
	@echo "$(GREEN)Datos de prueba insertados$(NC)"

# Comandos de monitoreo
logs: ## Ver logs de la aplicación
	@echo "$(YELLOW)Mostrando logs...$(NC)"
	tail -f logs/app.log || echo "$(RED)No se encontraron logs$(NC)"

# Comandos de backup
backup-db: ## Crear backup de la base de datos
	@echo "$(YELLOW)Creando backup de la base de datos...$(NC)"
	pg_dump panaderia_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Backup creado$(NC)"

# Comandos de deployment
deploy-check: test lint format-check ## Verificar que todo está listo para deployment
	@echo "$(GREEN)Todo listo para deployment$(NC)"

# Comandos de información
info: ## Mostrar información del proyecto
	@echo "$(GREEN)Sistema de Gestión de Productos de Panadería$(NC)"
	@echo "$(YELLOW)Versión:$(NC) 1.0.0"
	@echo "$(YELLOW)Framework:$(NC) FastAPI"
	@echo "$(YELLOW)Base de datos:$(NC) PostgreSQL"
	@echo "$(YELLOW)ORM:$(NC) SQLAlchemy"
	@echo "$(YELLOW)Migraciones:$(NC) Alembic"
	@echo "$(YELLOW)Tests:$(NC) Pytest"
	@echo "$(YELLOW)Documentación:$(NC) Swagger/OpenAPI"

# Comandos de ayuda específicos
help-db: ## Ayuda para comandos de base de datos
	@echo "$(GREEN)Comandos de base de datos:$(NC)"
	@echo "  make create-db    - Crear base de datos"
	@echo "  make drop-db      - Eliminar base de datos"
	@echo "  make check-db     - Verificar conexión"
	@echo "  make backup-db    - Crear backup"

help-migrate: ## Ayuda para comandos de migración
	@echo "$(GREEN)Comandos de migración:$(NC)"
	@echo "  make migrate      - Crear nueva migración"
	@echo "  make upgrade      - Aplicar migraciones"
	@echo "  make downgrade    - Revertir migración"
	@echo "  make history      - Ver historial"
	@echo "  make current      - Ver migración actual"

help-test: ## Ayuda para comandos de testing
	@echo "$(GREEN)Comandos de testing:$(NC)"
	@echo "  make test         - Ejecutar tests"
	@echo "  make test-cov     - Tests con cobertura"
	@echo "  make test-watch   - Tests en modo watch"

# Comando por defecto
.DEFAULT_GOAL := help

# FastAPI Course - API REST

Una API REST completa construida con FastAPI, SQLAlchemy y MySQL.

## 🚀 Instalación y Ejecución

### Opción 1: Instalación Automática (Recomendada)

```bash
# Ejecutar el script de instalación automática
python run_app.py
```

Este script verificará e instalará automáticamente todas las dependencias necesarias.

### Opción 2: Instalación Manual

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Ejecutar la aplicación:**
```bash
# Opción A: Usando el script simple
python start_server.py

# Opción B: Directamente con uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opción C: Con Python
python main.py
```

## 📋 Dependencias

- `fastapi>=0.104.0` - Framework web
- `uvicorn[standard]>=0.24.0` - Servidor ASGI
- `pydantic>=2.0.0` - Validación de datos
- `python-slugify>=8.0.0` - Generación de slugs
- `sqlalchemy>=2.0.0` - ORM para base de datos
- `pymysql>=1.1.0` - Driver MySQL

## 🗄️ Base de Datos

La aplicación requiere una base de datos MySQL con las siguientes credenciales:
- **Host:** localhost
- **Puerto:** 3306
- **Usuario:** root
- **Contraseña:** 123456
- **Base de datos:** fastapi

## 📚 Endpoints Disponibles

### Categorías
- `GET /categorias` - Listar todas las categorías
- `GET /categorias/{id}` - Obtener categoría por ID
- `POST /categorias` - Crear nueva categoría
- `PUT /categorias/{id}` - Actualizar categoría
- `DELETE /categorias/{id}` - Eliminar categoría

### Productos
- `GET /productos` - Listar todos los productos

### Ejemplos
- `GET /ejemplo` - Ejemplo GET
- `GET /ejemplo/{id}` - Ejemplo con parámetro
- `GET /ejemplo-query` - Ejemplo con query parameters
- `POST /ejemplo-form` - Ejemplo con formulario

## 🌐 Acceso

- **API:** http://localhost:8000
- **Documentación:** http://localhost:8000/docs
- **Documentación alternativa:** http://localhost:8000/redoc

## 🔧 Solución de Problemas

### Error: "No module named 'slugify'"
```bash
pip install python-slugify
```

### Error: "No module named 'pymysql'"
```bash
pip install pymysql
```

### Error de conexión a MySQL
Verifica que:
1. MySQL esté ejecutándose
2. Las credenciales en `database.py` sean correctas
3. La base de datos `fastapi` exista

### Warning de Pydantic
Si ves warnings sobre `schema_extra`, ya están corregidos en la versión actual.

## 📁 Estructura del Proyecto

```
FastAPI-course/
├── main.py              # Aplicación principal
├── api.py               # Endpoints de la API
├── database.py          # Configuración de base de datos
├── modelos.py           # Modelos SQLAlchemy
├── esquema.py           # Esquemas Pydantic
├── requirements.txt     # Dependencias
├── run_app.py          # Script de inicio automático
├── start_server.py     # Script de inicio simple
└── install_dependencies.bat  # Script de instalación (Windows)
```
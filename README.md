# Solución Prueba de Conocimiento – Ingeniero de Desarrollo de Software
# Proyecto: rds_handle_business

## Resumen del Proyecto

Este proyecto permite levantar un entorno MySQL con Docker, poblarlo con datos de ejemplo, ejecutar un pipeline ETL en Python para crear un data warehouse local y exponer la información a través de una API REST desarrollada en Python con FastAPI. El objetivo es demostrar habilidades en bases de datos, ETL y desarrollo de APIs.

## Explicación básica

En la raíz principal del proyecto se pueden apreciar 3 carpetas principales:

1. **rds_handle_business**: Contiene una base de datos relacional MySQL llamada `rds_handle_business` que se crea a través de Docker Compose junto con 3 tablas principales: `clientes`, `productos` y `ventas`. La información de ejemplo se inserta automáticamente por un script SQL ejecutado por Docker Compose. Las consultas SQL solicitadas en la Prueba de Conocimientos se encuentran en el directorio `sql_test_requests`.

2. **etl_pipeline_mysql**: Contiene la lógica necesaria para obtener todos los datos almacenados en la base de datos `rds_handle_business` y se encarga de crear una nueva base de datos relacional para almacenamiento de data warehouse llamada `rds_handle_business_dw`, donde se guardan exactamente las mismas tablas bajo el mismo esquema e información existente.

3. **api_handle_business**: Contiene una API desarrollada en Python encargada de retornar el total de las ventas realizadas según la categoría de productos.

## Estructura del proyecto

**1. api_handle_business**

- `config.ini` → Archivo de configuración para la API (base de datos, puertos, claves, etc.)
- `main.py` → Archivo principal que ejecuta la API, define rutas, endpoints y lógica del servicio.
- `requirements.txt` → Lista de dependencias de Python necesarias para la API.

**2. etl_pipeline_mysql**

- `config.ini` → Archivo de configuración del pipeline ETL (credenciales MySQL, tablas, rutas de archivos, etc.)
- `etl.py` → Script principal que ejecuta el proceso ETL (Extract, Transform, Load).
- `requirements.txt` → Dependencias de Python necesarias para ejecutar el pipeline.

**3. rds_handle_business**

- `docker-compose.yml` → Archivo de Docker Compose que levanta el contenedor de MySQL con la base de datos inicializada y persistente.
- `initdb/01-init.sql` → Script SQL que crea las tablas (`clientes`, `productos`, `ventas`) y carga datos iniciales.
- `sql_test_requests/` → Archivos `.sql` con las consultas solicitadas en la prueba.

## Requisitos

- Docker y Docker Compose instalados.
- Python 3.13 o superior.
- MySQL cliente (opcional, para probar la base de datos desde fuera del contenedor).

## Módulos/Librerías Python necesarios

- fastapi
- uvicorn
- mysql-connector-python

## Funcionamiento

### 1. Levantar el contenedor MySQL

Desde la carpeta `rds_handle_business` ejecutar:

```bash
docker-compose up -d
```
> Este comando levantará la instancia de MySQL y creará automáticamente la base de datos `rds_handle_business` con las tablas correspondientes y los datos iniciales.

### 2. Ejecución del ETL en Python

Desde la carpeta `etl_pipeline_mysql` ejecutar:

**1. Crear y activar el entorno virtual**

Linux:
```bash
python -m venv venv
source venv/bin/activate
```

Windows (CMD):
```bat
python -m venv venv
.\venv\Scripts\activate.bat
```

**2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**3. Ejecutar ETL**
```bash
python etl.py
```
> Esta ejecución creará en la misma instancia de Docker una base de datos idéntica llamada `rds_handle_business_dw`, que almacena todos los registros de la base original y puede consultarse para su validación.

### 3. Despliegue de la API local con FastAPI

Desde la carpeta `api_handle_business` ejecutar:

**1. Crear y activar el entorno virtual**
(Linux/Windows igual que en el paso ETL)

**2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**3. Inicializar servicios de la API**
```bash
uvicorn main:app --reload
```

**4. Probar la API**

- Documentación interactiva (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Endpoint de ejemplo: `GET /ventas/por-categoria`  [http://127.0.0.1:8000/ventas/por-categoria](http://127.0.0.1:8000/ventas/por-categoria)

> La API se conecta directamente a la base de datos `rds_handle_business_dw` creada por el ETL, permitiendo análisis histórico sin afectar la base de producción.

## Mejoras futuras

- Integración de un sistema de autenticación en la API (OAuth2, JWT) para seguridad.
- Soporte de más tablas y relaciones complejas en el Data Warehouse.
- Automatización de ETL periódica usando cron jobs o Airflow.
- Añadir tests unitarios y de integración para la API y el pipeline ETL.
- Despliegue en la nube (Docker Swarm, Kubernetes) para producción.
- Implementación de logging y monitoreo de la API y base de datos.
- Refactorizar la API y ETL para implementar **Clean Architecture**, separando responsabilidades, capas de dominio, infraestructura y presentación para mejorar mantenibilidad, escalabilidad y testeo.

## Autor

- **Nombre:** Michael Romero Ortega
- **Cargo:** Ingeniero de Sistemas / Desarrollador de Software
- **Fecha:** 28 de diciembre de 2025


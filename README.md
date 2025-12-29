# Solución Prueba de Conocimiento – Ingeniero de Desarrollo de Software
# Proyecto: rds_handle_business


## Resumen del Proyecto:

Este proyecto permite levantar un entorno MySQL con Docker, poblarlo con datos de ejemplo, ejecutar un pipeline ETL en Python para crear un data warehouse local y exponer la información a través de una API REST desarrollada en Python con FastAPI. El objetivo es demostrar habilidades en bases de datos, ETL y desarrollo de APIs.

## Explicación básica:

En la raiz principal del proyecto se pueden apreciar 3 carpetas principales:

1. rds_handle_business: Contiene una base de datos relacional mysql llamada rds_handle_business la cual es creada a traves de Docker Compose junto con 3 tablas principales: clientes, productos y ventas. La información de ejemplo es insertada automaticamente por un script sql ejecutado por Docker Compose. 
Las consultas SQL solicitadas en la Prueba de Conocimientos se encuentran en el directorio "sql_test_requests" disponibles para su respectiva validación.
2. etl_pipeline_mysql: Contiene la logica necesaria para obtener todos los datos almacenados en la base de datos rds_handle_business y se encarga de crear una nueva base de datos relacional para almacenamiento de data warehouse llamada rds_handle_business_dw en donde se guardan exactamente las mismas tablas bajo el mismo esquema e información existente.
3. api_handle_business: Contiene una API desarrollada en Python encargada de retornar el total de las ventas realizadas según la categoria de productos.

## Estructura del proyecto:

1. api_handle_business

config.ini → Archivo de configuración para la API, contiene parámetros como base de datos, puertos, claves, etc.
main.py → Archivo principal que ejecuta la API, define rutas, endpoints y lógica del servicio.
requirements → Lista de dependencias de Python necesarias para la API (requirements.txt o similar).

2. etl_pipeline_mysql
config.ini → Archivo de configuración para el pipeline ETL, como credenciales de MySQL, tablas, rutas de archivos, etc.
etl.py → Script principal que ejecuta el proceso ETL (Extract, Transform, Load), moviendo y transformando datos hacia una nueva base de datos para analitica warehouse MySQL.
requirements → Dependencias de Python necesarias para ejecutar el pipeline.

3. rds_handle_business

docker-compose.yml → Archivo de Docker Compose que levanta el contenedor de MySQL con la base de datos inicializada y persistente.
initdb/01-init.sql → Script SQL que crea las tablas (clientes, productos, ventas) y carga datos iniciales en MySQL.
sql_test_requests → Archivo .sql en donde se evidencian las consultas solicitadas.

## Requisitos:

- Docker y Docker Compose instalados.
- Python 3.13 o superior.
- MySQL cliente (opcional, para probar la base de datos desde fuera del contenedor).

## Modulos/Librerias Python necesarios:

- fastapi
- uvicorn
- mysql-connector-python

## Funcionamiento: 

## 1. Levantar el contenedor MySQL

Desde la carpeta `rds_handle_business` ejecutar:

```bash
docker-compose up -d
# Este comando se encargara de levantar la instancia de base de datos MYSQL y creará automaticamente la base de datos rds_handle_business junto a las tablas correspondientes y filas de inserción requeridas para efectuar las pruebas correspondientes.
```
## 2. Ejecución de ETL Python:

Desde la carpeta `etl_pipeline_mysql` ejecutar:

1. Creación y activación del entorno de desarrollo:
# Linux:
python -m venv venv
source venv/bin/activate
# Windows (CMD):
python -m venv venv
.\venv\Scripts\activate.bat
2. # Instalar requisitos:
pip install -r requirements
3. # Ejecutar ETL:
python etl.py
```
# Esta ejecución se encargara de crear en la misma instancia de Docker una base de datos identica a la origial, la cual almacenará todos los registros insertados inicialmente y tendrá el nombre rds_handle_business_dw, la misma puede ser consultada a traves de la instancia creada a traves de Docker Compose para su respectiva validación.
```
## 3. Despliegue API Local (Prueba) fastapi:

Desde la carpeta `api_handle_business` ejecutar:

1. Creación y activación del entorno de desarrollo:
# Linux:
python -m venv venv
source venv/bin/activate
# Windows (CMD):
python -m venv venv
.\venv\Scripts\activate.bat
2. # Instalar requisitos:
pip install -r requirements
3. # Inicializar servicios API a través del comando:
uvicorn main:app --reload
4. # Prueba funcional API:
Una vez inicializados los servicios correspondientes a la API, será posible evidenciar a traves de la documentación de la API la forma mediante la cual es posible realizar la respectiva petición, además la siguiente interfaz web permitira interactuar con la API validando el resultado puntual de salida:
http://127.0.0.1:8000/docs
Esta API se encarga de establecer conexión directa hacia la base de datos creada mediante la ETL ejecutada en el paso 2 (rds_handle_business_dw), de esta manera será posible realizar analisis de datos de manera precisa y eficiente a nivel historico sin afectar producción.
La prueba funcional tambien puede realizarse accediendo directamente al recurso (/ventas/por-categoria) implementado en el codigo fuente de la API, de esta manera sera posible retornar los datos desde un navegador web automaticamente:
http://127.0.0.1:8000/ventas/por-categoria

## Mejoras futuras:

- Integración de un sistema de autenticación en la API (OAuth2, JWT) para seguridad.
- Soporte de más tablas y relaciones complejas en el Data Warehouse.
- Automatización de ETL periódica usando cron jobs o Airflow.
- Añadir tests unitarios y de integración para la API y el pipeline ETL.
- Despliegue en la nube (Docker Swarm, Kubernetes) para producción.
- Implementación de logging y monitoreo de la API y base de datos.
- Refactorizar la API y ETL para implementar Clean Architecture, separando responsabilidades, capas de dominio, infraestructura y presentación para mejorar mantenibilidad, escalabilidad y testeo.

## Autor

- Nombre: Michael Romero Ortega
- Ingeniero de Sistemas / Desarrollador de Software
- Fecha: 28 de diciembre de 2025

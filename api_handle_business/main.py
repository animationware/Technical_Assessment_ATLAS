from fastapi import FastAPI
import mysql.connector
import configparser

# Creamos la instancia de la API con un título descriptivo
app = FastAPI(title="API Ventas por Categoría")

# Creamos un objeto ConfigParser para leer archivos de configuración
config = configparser.ConfigParser()

# Leemos el archivo "config.ini" que contiene los datos de la base de datos
config.read("config.ini")

# Accedemos a la sección "database" dentro del archivo ini
db_config = config["database"]

def get_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL
    usando los parámetros definidos en config.ini
    """
    return mysql.connector.connect(
        host=db_config["host"],         # Dirección del servidor de la base de datos
        port=db_config["port"],         # Puerto de conexión (normalmente 3306)
        database=db_config["database"], # Nombre de la base de datos
        user=db_config["user"],         # Usuario autorizado para la base de datos
        password=db_config["password"]  # Contraseña del usuario
    )

@app.get("/ventas/por-categoria")
def ventas_por_categoria():
    """
    Endpoint que devuelve el total de ventas agrupadas por categoría de productos.
    """
    # Abrimos la conexión con la base de datos
    conn = get_connection()

    # Creamos un cursor que devuelve los resultados como diccionarios
    cursor = conn.cursor(dictionary=True)

    # Consulta SQL para obtener el total de ventas por categoría
    query = """
        SELECT
            p.categoria,                     -- Nombre de la categoría
            SUM(v.cantidad * p.precio) AS total_ventas  -- Total de ventas por categoría
        FROM ventas v
        JOIN productos p ON v.id_producto = p.id_producto  -- Relacionamos ventas con productos
        GROUP BY p.categoria                -- Agrupamos los resultados por categoría
        ORDER BY total_ventas DESC           -- Ordenamos de mayor a menor total de ventas
    """

    # Ejecutamos la consulta SQL
    cursor.execute(query)

    # Obtenemos todos los resultados de la consulta
    result = cursor.fetchall()

    # Cerramos el cursor y la conexión para liberar recursos
    cursor.close()
    conn.close()

    # Retornamos los resultados en formato JSON
    return result

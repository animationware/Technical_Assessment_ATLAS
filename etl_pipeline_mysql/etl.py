import configparser
import mysql.connector

# Creamos un objeto ConfigParser para leer la configuración desde un archivo .ini
config = configparser.ConfigParser()

## Leemos el archivo "config.ini" que contiene los datos de conexión a las bases de datos
config.read("config.ini")

def create_database_if_not_exists():
    """
    Verifica si la base de datos destino existe; si no, la crea.
    """
    # Obtenemos una conexión al servidor MySQL sin especificar base de datos
    conn = get_connection("target_db", with_db=False)

    # Creamos un cursor para ejecutar comandos SQL
    cursor = conn.cursor()

    # Obtenemos el nombre de la base de datos destino desde el archivo de configuración
    db_name = config["target_db"]["database"]

    # Ejecutamos la sentencia SQL para crear la base de datos si no existe
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    # Confirmamos los cambios en el servidor
    conn.commit()

    # Cerramos el cursor y la conexión para liberar recursos
    cursor.close()
    conn.close()

def get_connection(section, with_db=True):
    """
    Devuelve una conexión a MySQL usando la sección de configuración indicada.
    Si with_db es False, no selecciona ninguna base de datos al conectarse.
    """
    return mysql.connector.connect(
        host=config[section]["host"],                       # Dirección del servidor
        port=config[section]["port"],                       # Puerto de conexión
        database=config[section]["database"] if with_db else None,  # Base de datos opcional
        user=config[section]["user"],                       # Usuario autorizado
        password=config[section]["password"]                # Contraseña del usuario
    )

def extract_data(conn):
    """
    Extrae todos los datos de las tablas 'clientes', 'productos' y 'ventas'
    desde la conexión proporcionada.
    """
    # Creamos un cursor que devuelve los resultados como diccionarios
    cursor = conn.cursor(dictionary=True)

    tables = {}  # Diccionario donde guardaremos los datos de cada tabla

    # Iteramos sobre las tablas que queremos extraer
    for table in ["clientes", "productos", "ventas"]:
        # Ejecutamos la consulta para traer todos los registros
        cursor.execute(f"SELECT * FROM {table}")
        # Guardamos los resultados en el diccionario
        tables[table] = cursor.fetchall()

    # Cerramos el cursor
    cursor.close()

    # Retornamos los datos extraídos
    return tables

def create_target_tables(conn):
    """
    Crea las tablas en la base de datos destino si no existen.
    """
    cursor = conn.cursor()

    # Creamos la tabla 'clientes' con columnas y tipos de datos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INT PRIMARY KEY,
            nombre VARCHAR(100),
            ciudad VARCHAR(100),
            fecha_registro DATETIME
        )
    """)

    # Creamos la tabla 'productos'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INT PRIMARY KEY,
            categoria VARCHAR(100),
            precio DECIMAL(10,2)
        )
    """)

    # Creamos la tabla 'ventas'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INT PRIMARY KEY,
            id_cliente INT,
            id_producto INT,
            fecha_venta DATETIME,
            cantidad INT
        )
    """)

    # Confirmamos los cambios
    conn.commit()

    # Cerramos el cursor
    cursor.close()

def load_data(conn, data):
    """
    Inserta los datos extraídos en las tablas destino, actualizando si ya existen.
    """
    cursor = conn.cursor()

    # Insertamos los clientes, actualizando los existentes si es necesario
    cursor.executemany("""
        INSERT INTO clientes VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        nombre = VALUES(nombre),
        ciudad = VALUES(ciudad),
        fecha_registro = VALUES(fecha_registro)
    """, [
        (c["id_cliente"], c["nombre"], c["ciudad"], c["fecha_registro"])
        for c in data["clientes"]
    ])

    # Insertamos los productos, actualizando si ya existen
    cursor.executemany("""
        INSERT INTO productos VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        categoria = VALUES(categoria),
        precio = VALUES(precio)
    """, [
        (p["id_producto"], p["categoria"], p["precio"])
        for p in data["productos"]
    ])

    # Insertamos las ventas, actualizando si ya existen
    cursor.executemany("""
        INSERT INTO ventas VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        id_cliente = VALUES(id_cliente),
        id_producto = VALUES(id_producto),
        fecha_venta = VALUES(fecha_venta),
        cantidad = VALUES(cantidad)
    """, [
        (v["id_venta"], v["id_cliente"], v["id_producto"],
         v["fecha_venta"], v["cantidad"])
        for v in data["ventas"]
    ])

    # Confirmamos los cambios
    conn.commit()

    # Cerramos el cursor
    cursor.close()

def main():
    """
    Flujo principal del ETL:
    1. Conectar a la base de datos origen
    2. Extraer los datos
    3. Crear base de datos destino si no existe
    4. Conectar a la base de datos destino
    5. Crear tablas destino
    6. Cargar los datos extraídos
    """
    print("🔹 Conectando a base de datos origen...")
    source_conn = get_connection("source_db")

    print("🔹 Extrayendo datos...")
    data = extract_data(source_conn)
    source_conn.close()

    print("🔹 Verificando base de datos destino...")
    create_database_if_not_exists()

    print("🔹 Conectando a base de datos destino...")
    target_conn = get_connection("target_db")

    print("🔹 Creando tablas destino...")
    create_target_tables(target_conn)

    print("🔹 Cargando datos...")
    load_data(target_conn, data)

    target_conn.close()
    print("✅ ETL finalizado correctamente.")

# Ejecutamos el flujo principal si se llama directamente este script
if __name__ == "__main__":
    main()

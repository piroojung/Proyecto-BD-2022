import mariadb
import sys

USER = "cris"
PASSWORD = "cris"

try:
    connection = mariadb.connect(
        user=USER,
        password=PASSWORD,
        host="localhost",
        port=3306,
    )

except mariadb.Error as e:
    print(f"Error de conexión a la plataforma de MariaDB: {e}")
    sys.exit(1)

cursor = connection.cursor()

# Crear base de datos
try:
    cursor.execute("CREATE DATABASE model")
except mariadb.ProgrammingError:
    print("Base de datos ya creada...")

# Usar base de datos 
cursor.execute("USE model")

# Crear tablas
cursor.execute(
    """CREATE TABLE IF NOT EXISTS duenos(
       id_dueno INT, 
       nombreDueno VARCHAR(50), 
       tipoDueno CHAR BYTE
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS medios(
        id_medio INT, 
        nombrePrensa VARCHAR(50), 
        idiomaPrincipal CHAR BYTE,
        fechaCreacion DATE,
        urlPrensa VARCHAR(100),
        codigoRegion INT,
        pais VARCHAR(15),
        region VARCHAR(30),
        id_noticia INT
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS noticias(
        id_noticia INT, 
        tituloNoticia VARCHAR(50), 
        urlNoticia VARCHAR(100),
        fechaPublicacion DATE,
        contenidoTextual VARCHAR(5000)
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS personas(
        id_persona INT, 
        nombreMencion VARCHAR(50), 
        tienePaginaWikipedia BOOLEAN,
        nacionalidad VARCHAR(20),
        profesion VARCHAR(50),
        fechaNacimiento DATE,
        id_popularidad INT
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS popularidad(
       id_popularidad INT, 
       fecha DATE,
       cantidadVisitas INT
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS poseer(
       id_dueno INT, 
       id_medio INT,
       fechaVenta DATE,
       fechaAdquisicion DATE
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS menciones(
       id_noticia INT, 
       id_persona INT
    )""")


cursor.execute("SHOW TABLES")
for row in cursor:
    print(row)



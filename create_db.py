import mariadb
import sys

USER = "dui"
PASSWORD = "benja123"

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
try:
    cursor.execute("DROP TABLE duenos")
    cursor.execute("DROP TABLE medios")
    cursor.execute("DROP TABLE noticias")
    cursor.execute("DROP TABLE personas")
    cursor.execute("DROP TABLE popularidad")
    cursor.execute("DROP TABLE poseer")
    cursor.execute("DROP TABLE menciones")
except: pass
# Crear tablas
cursor.execute(
    """CREATE TABLE IF NOT EXISTS duenos(
       id_dueno INT NOT NULL AUTO_INCREMENT, 
       nombreDueno VARCHAR(50), 
       tipoDueno CHAR BYTE,
       PRIMARY KEY(id_dueno)
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS medios(
        id_medio INT NOT NULL AUTO_INCREMENT, 
        nombrePrensa VARCHAR(50), 
        idiomaPrincipal VARCHAR(20),
        fechaCreacion DATE,
        urlPrensa VARCHAR(100),
        codigoRegion INT,
        pais VARCHAR(15),
        region VARCHAR(30),
        PRIMARY KEY(id_medio)
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS noticias(
        id_noticia INT NOT NULL AUTO_INCREMENT, 
        tituloNoticia VARCHAR(50), 
        urlNoticia VARCHAR(100),
        fechaPublicacion DATE,
        contenidoTextual TEXT,
        id_medio INT,
        PRIMARY KEY(id_noticia)
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS personas(
        id_persona INT NOT NULL AUTO_INCREMENT, 
        nombreMencion VARCHAR(50), 
        tienePaginaWikipedia BOOLEAN,
        nacionalidad VARCHAR(20),
        profesion VARCHAR(50),
        fechaNacimiento DATE,
        PRIMARY KEY(id_persona)
    )""")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS popularidad(
       id_popularidad INT NOT NULL AUTO_INCREMENT, 
       fecha DATE,
       cantidadVisitas INT,
       id_persona INT,
       PRIMARY KEY(id_popularidad)
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



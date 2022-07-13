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
        database="model"
    )

except mariadb.Error as e:
    print(f"Error de conexión a la plataforma de MariaDB: {e}")
    sys.exit(1)

cursor = connection.cursor()

cursor.execute("INSERT INTO duenos (nombreDueno, tipoDueno) VALUES ('Asdasda', 'N')")
cursor.execute(
    "INSERT INTO medios (nombrePrensa, idiomaPrincipal, fechaCreacion, urlPrensa, codigoRegion, pais, region)\
     VALUES ('Hola mundo', 'Español', '1995-06-22', 'www.holamundo.cl', 14, 'Chile', 'XIV') \
     ")
cursor.execute(
    "INSERT INTO noticias (tituloNoticia, urlNoticia, fechaPublicacion, contenidoTextual, id_medio)\
     VALUES ('Nananana', 'www.holamundo.cl/nananana', '1995-06-22', 'akaajkjajajajaja', 3) \
     ")
cursor.execute(
    "INSERT INTO personas (nombreMencion, tienePaginaWikipedia, nacionalidad, profesion, fechaNacimiento)\
     VALUES ('Qwerty Uiop', TRUE, 'chilena', 'Medico', CURRENT_TIMESTAMP) \
     ")
cursor.execute(
    "INSERT INTO popularidad (fecha, cantidadVisitas, id_persona)\
     VALUES (CURRENT_TIMESTAMP, 15, 1) \
     ")

cursor.execute(
    "INSERT INTO poseer (id_dueno, id_medio, fechaVenta, fechaAdquisicion)\
     VALUES (1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) \
     ")

cursor.execute(
    "INSERT INTO menciones (id_noticia, id_persona)\
     VALUES (1, 1) \
     ")



connection.commit()

#cursor.execute("DESCRIBE duenos")
cursor.execute("SELECT * FROM duenos")
for row in cursor: print(row)

cursor.execute("SELECT * FROM medios")
for row in cursor: print(row)

cursor.execute("SELECT * FROM noticias")
for row in cursor: print(row)

cursor.execute("SELECT * FROM personas")
for row in cursor: print(row)

cursor.execute("SELECT * FROM popularidad")
for row in cursor: print(row)

cursor.execute("SELECT * FROM poseer")
for row in cursor: print(row)

cursor.execute("SELECT * FROM menciones")
for row in cursor: print(row)
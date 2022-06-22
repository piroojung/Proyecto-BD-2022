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

# a) 
cursor.execute(
    "SELECT nombrePrensa, count(*) FROM noticias JOIN medios ON \
    noticias.id_medio = medios.id_medio GROUP BY noticias.id_medio"
)
for row in cursor: print(row)

# b)
cursor.execute(
    "SELECT nombreMencion, tituloNoticia FROM personas JOIN menciones \
    ON personas.id_persona = menciones.id_persona JOIN noticias ON \
    menciones.id_noticia = noticias.id_noticia WHERE noticias.fechaPublicacion = '2022-06-19'"
)
for row in cursor: print(row)

# c)
cursor.execute(
    "SELECT fecha, cantidadVisitas FROM popularidad WHERE id_persona=1"
)
for row in cursor: print(row)

# # d)
# cursor.execute(

# )
# for row in cursor: print(row)
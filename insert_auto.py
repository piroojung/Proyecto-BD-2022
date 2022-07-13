from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers import pipeline
from tqdm import tqdm
import wikipedia
import mariadb
import sys
import pageviewapi

from extract_persons import persons
from scrappers.antofagasta_enlalinea import noticias



def get_date(str_date):
    months =  {"enero":"01","febrero":"02", "marzo":"03","abril":"04","mayo":"05","junio":"06",
        "julio":"07","agosto":"08","septiembre":"09","octubre":"10","noviembre":"11","diciembre":"12"
    }
    day = month = "01"
    year = None
    for str_ in str_date.split(" "):
        if(str_.isnumeric()):
            if(len(str_) > 2):
                year = str_
            else:
                day = str_
        elif(months.get(str_, None) is not None):
            month = months[str_]

    return f"{year}-{month}-{day}" if year is not None else None




print("\nextract_persons.py OK")

################ WIKIPEDIA ################
wikipedia.set_lang("es")
print("wikipedia OK")

################ TRANSFORMERS ################
ES_MODEL_LANGUAGE="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
tokenizer_es_language = AutoTokenizer.from_pretrained(ES_MODEL_LANGUAGE)
model_es_language = AutoModelForQuestionAnswering.from_pretrained(ES_MODEL_LANGUAGE)
q_a_es = pipeline("question-answering", model=model_es_language, tokenizer=tokenizer_es_language)
print("transformers OK")

################ MARIADB ################
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
print("mariadb OK")

import warnings
warnings.filterwarnings("ignore")


try:
    import create_db
    del create_db
    print("(i) Base de datos reiniciada")
except:
    print("(i) No se pudo reiniciar la base de datos")


################ TABLA PERSONAS / POPULARIDAD ################
print()
print("---------------------------------------------------------")
print("------- GENERANDO TABLAS PERSONAS Y POPULARIDAD ---------")
print("---------------------------------------------------------")
print()
id_persona = {}
all_persons = []
for person_list in persons.values():
    all_persons += person_list

i = 1
for person in tqdm(all_persons):
    wiki = "FALSE"
    try:
        results = wikipedia.search(person)
        summary = wikipedia.summary(results[0], sentences=3)

        #preguntas
        result = q_a_es(question="¿En qué fecha nació el o ella?", context=summary)
        f_nac = result["answer"]

        result = q_a_es(question="¿Cuál es su profesión?", context=summary)
        prof = result["answer"]

        result = q_a_es(question="¿Cuál es su nacionalidad?", context=summary)
        nacdd = result["answer"]

    except IndexError:
        nacdd = prof = f_nac = "NULL"

    except KeyboardInterrupt:
        break
    
    except:
        continue
    
    try:
        result=pageviewapi.per_article('es.wikipedia', person, '20220701', '20220730',
                        access='all-access', agent='all-agents', granularity='daily')
        day = 1
        for item in result.items():
            for article in item[1]:
                views=article['views']
                cursor.execute(
                    f"INSERT INTO popularidad (fecha, cantidadVisitas, id_persona)\
                    VALUES ('2022-07-{'0'+str(day) if day < 10 else str(day)}', {views}, {i}) \
                    ")
                day += 1
        
        wiki = "TRUE"

    except pageviewapi.client.ZeroOrDataNotLoadedException:
        pass

    connection.commit()

    try:
        cursor.execute(
            f"INSERT INTO personas (nombreMencion, tienePaginaWikipedia, nacionalidad, profesion, fechaNacimiento)\
            VALUES ('{person}', {wiki}, '{nacdd}', '{prof}', '{get_date(f_nac)}') \
            ")
        id_persona[person] = i
        i += 1

    except mariadb.OperationalError:
        cursor.execute(
            f"INSERT INTO personas (nombreMencion, tienePaginaWikipedia, nacionalidad, profesion, fechaNacimiento)\
            VALUES ('{person}', {wiki}, '{nacdd}', '{prof}', NULL) \
            ")
        id_persona[person] = i
        i += 1

    except mariadb.DataError:
        continue



################ TABLA NOTICIAS ################
print()
print("---------------------------------------------------------")
print("-------------- GENERANDO TABLA NOTICIAS -----------------")
print("---------------------------------------------------------")
print()
 
for title, url, date, text in tqdm(noticias):
    try:
        cursor.execute(
            f"INSERT INTO noticias (tituloNoticia, urlNoticia, fechaPublicacion, contenidoTextual, id_medio)\
            VALUES ('{title}', '{url}', '{get_date(date)}', '{text}', 1) \
            ")
    
    except mariadb.OperationalError:
        cursor.execute(
            f"INSERT INTO noticias (tituloNoticia, urlNoticia, fechaPublicacion, contenidoTextual, id_medio)\
            VALUES ('{title}', '{url}', NULL, '{text}', 1) \
            ")

    connection.commit()



################ TABLA MEDIOS ################
medios = [
    ['En la Linea Antofagasta', 'Español', 'https://enlalinea.cl/', 3, 'Chile', 'Antofagasta'],
    ['El Nortero', 'Español', 'https://www.elnortero.cl/', 3, 'Chile', 'Antofagasta'],
    ['El America', 'Español', 'https://elamerica.cl/', 3, 'Chile', 'Antofagasta'],
]

print()
print("---------------------------------------------------------")
print("--------------- GENERANDO TABLA MEDIOS ------------------")
print("---------------------------------------------------------")
print()
 
for nombre, idioma, url, c_reg, pais, n_reg in tqdm(medios):
    cursor.execute(
        f"INSERT INTO medios (nombrePrensa, idiomaPrincipal, fechaCreacion, urlPrensa, codigoRegion, pais, region)\
        VALUES ('{nombre}', '{idioma}', NULL, '{url}', {c_reg}, '{pais}', '{n_reg}') \
        ")

    connection.commit()



################ TABLA MENCIONES ################
print()
print("---------------------------------------------------------")
print("--------------- GENERANDO TABLA MENCIONES ------------------")
print("---------------------------------------------------------")
print()
for id_noticia, personas in persons.items():
    for person in personas:
        if(id_persona.get(person, None) is not None):
            cursor.execute(
                f"INSERT INTO menciones (id_noticia, id_persona)\
                VALUES ({id_noticia}, {id_persona[person]}) \
                ")
            connection.commit()


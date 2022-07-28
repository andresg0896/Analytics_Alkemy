# Se importan los modulos a usar.
import descarga
import procesamiento
import conexion
import logging
from DB_URL import *

# Se crea el archivo donde se guardaran los logs.
logging.basicConfig(filename = 'comentarios.log', encoding = 'utf-8', level = logging.DEBUG)

# Se descargan los csv de las url proporcionadas y se registra un log.
descarga.obtencion_csv('museos', url_museo)
descarga.obtencion_csv('cines', url_cine)
descarga.obtencion_csv('bibliotecas', url_biblioteca)
logging.info('Descarga de tablas efectuada correctamente.')

# Se procesan las tablas y se crean los nuevos csv.
procesamiento.procesamiento_tablas()
logging.info('Procesamiento de tablas efectuado correctamente.')

# Se realiza la conexión y carga a la Base de datos de PostgreSQL
conexion.conexion_bd()
logging.info('Conexión a base de datos efectuada correctamente.')





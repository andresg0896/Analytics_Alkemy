# Se importan los modulos a usar
import descarga
import procesamiento
import conexion
import logging
from DB_URL import *

logging.basicConfig(filename = 'comentarios.log', encoding = 'utf-8', level = logging.DEBUG)

descarga.obtencion_csv('museos', url_museo)
descarga.obtencion_csv('cines', url_cine)
descarga.obtencion_csv('bibliotecas', url_biblioteca)
logging.info('Descarga de tablas efectuada correctamente.')
procesamiento.procesamiento_tablas()
logging.info('Procesamiento de tablas efectuado correctamente.')
conexion.conexion_bd()
logging.info('Conexión a base de datos efectuada correctamente.')





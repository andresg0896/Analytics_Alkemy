# Se importan los modulos necesarios
import os 
import requests
from datetime import date

# Se genera información de la fecha de descarga de los archivos para crear estos y sus carpetas.
mes = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

fecha_carga = date.today()

# Debido a que vamos a descargar 3 csv de categorias y url distintas (las que pueden cambiar), se crea una función que optimice este proceso.
def obtencion_csv(categoria, url):
    '''
    Genera la ruta de los archivos csv y los descarga a partir del ingreso de la categoría
    a la que pertenecen y su url.
    '''
    ruta = categoria + '/' + str(fecha_carga.year) + '-' + mes[(fecha_carga.month) - 1]
    # Si la carpeta no existe, se crea.
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    archivo = ruta + '/' + categoria + '-' + str(fecha_carga.day) + '-' + str(fecha_carga.month) + '-' + str(fecha_carga.year) + '.csv'
    # Se procede a descargar y guardar el csv.
    descarga = requests.get(url, allow_redirects=True)
    archivo_csv = open(archivo, 'wb')
    archivo_csv.write(descarga.content)
    archivo_csv.close()

import pandas as pd
import numpy as np
from datetime import date

# Se genera información de la fecha de descarga de los archivos para crear estos y sus carpetas.
mes = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

fecha_carga = date.today()

def procesamiento_tablas():
    '''
    Procesa y guarda los archivos csv de las 3 categorías
    y genera los 3 archivos csv nuevos con los totales.
    '''
    # Se escribe la ruta de los archivos ya descargados para crear los dataframe.
    ruta_museo = 'museos' + '/' + str(fecha_carga.year) + '-' + mes[(fecha_carga.month) - 1]
    archivo_museo = ruta_museo + '/' + 'museos' + '-' + str(fecha_carga.day) + '-' + str(fecha_carga.month) + '-' + str(fecha_carga.year) + '.csv'
    ruta_cine = 'cines' + '/' + str(fecha_carga.year) + '-' + mes[(fecha_carga.month) - 1]
    archivo_cine = ruta_cine + '/' + 'cines' + '-' + str(fecha_carga.day) + '-' + str(fecha_carga.month) + '-' + str(fecha_carga.year) + '.csv'
    ruta_biblioteca = 'bibliotecas' + '/' + str(fecha_carga.year) + '-' + mes[(fecha_carga.month) - 1]
    archivo_biblioteca = ruta_biblioteca + '/' + 'bibliotecas' + '-' + str(fecha_carga.day) + '-' + str(fecha_carga.month) + '-' + str(fecha_carga.year) + '.csv'
    # Se procede a leer los csv con su ruta.
    museos = pd.read_csv(archivo_museo, encoding='UTF-8')
    cines = pd.read_csv(archivo_cine, encoding='UTF-8')
    bibliotecas = pd.read_csv(archivo_biblioteca, encoding='UTF-8')
    # Se toman las columnas a necesitar de las tablas.
    museos_df = museos[['Cod_Loc', 'IdProvincia', 'IdDepartamento', 'categoria', 'provincia', 'localidad', 'nombre', 'direccion', 'CP', 'telefono', 'Mail', 'Web', 'fuente']]
    cines_df = cines[['Cod_Loc', 'IdProvincia', 'IdDepartamento', 'Categoría', 'Provincia', 'Localidad', 'Nombre', 'Dirección', 'CP', 'Teléfono', 'Mail', 'Web', 'Fuente']]
    salas_de_cine_df = cines[['Provincia', 'Pantallas', 'Butacas', 'espacio_INCAA']]
    bibliotecas_df = bibliotecas[['Cod_Loc', 'IdProvincia', 'IdDepartamento', 'Categoría', 'Provincia', 'Localidad', 'Nombre', 'Domicilio', 'CP', 'Teléfono', 'Mail', 'Web', 'Fuente']]
    # Se cambian los nombres de las columnas de todas las tablas a uno normalizado.
    nombre_normalizado = ['cod_localidad', 'id_provincia', 'id_departamento', 'categoría', 'provincia', 'localidad', 'nombre', 'domicilio', 'código postal', 'número de teléfono', 'mail', 'web', 'fuente']
    cines_df.columns = nombre_normalizado
    museos_df.columns = nombre_normalizado
    bibliotecas_df.columns = nombre_normalizado
    salas_de_cine_df.columns = ['provincia', 'nro_pantallas', 'nro_butacas', 'espacio_INCAA']
    # Se unen las 3 tablas de información en una sola.
    unica_df = pd.concat([museos_df, cines_df, bibliotecas_df])
    # Hay valores como s/d, los reemplazamos como nulos.
    # Los valores 'Sin domicilio' los dejamos, pues cuentan como valor.
    unica_df.replace('s/d', np.nan, inplace=True)
    # Hay 1 espacio INCAA como '0', por lo tanto lo reemplazamos por null, el cual consideraremos como 'no'.
    # Hay valores que dicen SI y otros si, vamos a dejar solo si.
    salas_de_cine_df.replace('0', np.nan, inplace=True)
    salas_de_cine_df.replace('SI', 'si', inplace=True)
    # Las provincias estan repetidas, por lo que agruparemos la tabla por provincia para que no repitan
    # Además, se suma el numero de pantallas y butacas, y se cuenta la cantidad de espacios_INCAA
    salas_de_cine_df = salas_de_cine_df.groupby('provincia').aggregate({'nro_pantallas': 'sum', 'nro_butacas':'sum', 'espacio_INCAA':'count'}).reset_index()
    # Hay en provincia valores como Santa Fe cuando tambien está Santa Fé. Corregimos
    # Tambien hay en provincia Tierra del Fuego cuando está Tierra del Fuego, Antártida... Lo agregamos a ese.
    unica_df.provincia.replace('Santa Fe', 'Santa Fé', inplace=True)
    unica_df.provincia.replace('Tierra del Fuego', 'Tierra del Fuego, Antártida e Islas del Atlántico Sur', inplace=True)
    # Se crean tablas que agrupan totales por categoría, por fuente, y por ambas.
    total_categoria = pd.DataFrame(unica_df.categoría.value_counts()).reset_index()
    total_categoria.columns = ['categoría', 'total_categoría']

    total_fuente = pd.DataFrame(unica_df.fuente.value_counts()).reset_index()
    total_fuente.columns = ['fuente', 'total_fuente']

    total_provincia_categoria = unica_df.value_counts(['provincia', 'categoría']).reset_index(name='total_provincia_y_categoría')
    # Luego de generar los totales, se borra la columna fuente.
    unica_df.drop('fuente', axis=1, inplace=True)
    # Se normaliza la tabla de provincia y categoría, creando una unica columna conjunta.
    total_provincia_categoria.insert(0, 'provincia_y_categoría', total_provincia_categoria[['provincia', 'categoría']].apply('/'.join, axis=1)) 
    total_provincia_categoria.drop(columns=['provincia','categoría'], axis=1, inplace=True)
    # Se unen las 3 tablas de totales generadas.
    registros_totales_df = pd.concat([total_categoria, total_fuente, total_provincia_categoria], axis=1)

    # Ahora le agregamos la columna fecha de carga a todos.
    unica_df = unica_df.assign(fecha_carga = date.today())
    registros_totales_df = registros_totales_df.assign(fecha_carga = date.today())
    salas_de_cine_df = salas_de_cine_df.assign(fecha_carga = date.today())

    #Por ultimo, creamos los csv.
    unica_df.to_csv('información_unificada.csv', index=False, encoding='UTF-8')
    registros_totales_df.to_csv('registros_totales.csv', index=False, encoding='UTF-8')
    salas_de_cine_df.to_csv('cantidad_salas_de_cine.csv', index=False, encoding='UTF-8')
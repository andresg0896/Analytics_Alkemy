import pandas as pd
from sqlalchemy import create_engine
from DB_URL import *

engine = create_engine('postgresql://' + pg_usuario + ':' + pg_clave + '@' + pg_host + ':' + pg_puerto + '/' + pg_bd)

def conexion_bd():
    unica_df = pd.read_csv('información_unificada.csv')
    registros_totales_df = pd.read_csv('registros_totales.csv')
    salas_de_cine_df = pd.read_csv('cantidad_salas_de_cine.csv')
    unica_df.to_sql('informacion_unificada', con=engine, if_exists='replace')
    registros_totales_df.to_sql('registros_totales', con=engine, if_exists='replace')
    salas_de_cine_df.to_sql('cantidad_salas_de_cine', con=engine, if_exists='replace')
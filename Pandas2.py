import pandas as pd
from sqlalchemy import create_engine
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage
import sys, os
from time import time
from sqlalchemy import create_engine

# #########################################################################################################
# Inserto lista de csv loteando con chunksize para que no muera.

#engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
#engine.connect()

#engine.dispose()
filePath = '/home/julian/workspaces/prueba_python/datasources/yellow_tripdata_{}.csv.gz'
#filePath = '/home/julian/Documents/jcZoomcamp2024/01-docker-terraform/ny-taxi-data/green_tripdata/green_tripdata_{}.csv.gz'

#yearMonths = [year + '-' + str(month).zfill(2) for year in ['2019', '2020'] for month in range(1,13)]
yearMonths = [year + '-' + str(month).zfill(2) for year in ['2021'] for month in range(1,2)]

# #########################################################################################################
# #defino inicialmente a la tabla (solo cuando quiero arrancar de cero!!!)
# df = pd.read_csv(filePath.format('2019-01'), sep=",", compression="gzip", nrows=1)

# df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
# df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
# df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

# # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
# # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
# # df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')
# #########################################################################################################
# sys.exit()

try:
    #cargo por lote
    for yearMonth in yearMonths:
        print('Reading csv: {} '.format(filePath.format(yearMonth)))
        
        df_iter = pd.read_csv(filePath.format(yearMonth), sep=",", compression="gzip", iterator=True, chunksize=500000)
        for df in df_iter:
            t_start = time()

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
#            df['tpep_pickup_date'] = df['tpep_pickup_datetime'].dt.date
#            df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')    

            # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            # df.to_sql(name='green_taxi_data', con=engine, if_exists='append')    

            t_end = time()
            print('inserted another chunk..., took %.3f seconds' % (t_end - t_start))
finally:
    None
#    engine.dispose()

# #------------------------------------------------------------------------------------------------------------------

# # engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
# # engine.connect()

# # # df = pd.read_csv('https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-10.csv.gz')
# # # print(df.head(10))
# # # print(df.info)

# # query = """
# #     SELECT *
# #       FROM mage.green_taxi
# #     LIMIT 100
# # """

# # df = pd.read_sql(query, con=engine)
# # print(df)

# #------------------------------------------------------------------------------------------------------------------

# # Ruta al archivo Parquet en Google Cloud Storage
# bucket_name = 'mage-zoomcamp-jc'
# objet_name_read = 'nyc_green_taxi_data_2022'
# key_path = '02-workflow-orchestration/iconic-atrium-414416-2428e49b5922.json'
# local_filename = 'archivo.parquet'

# # Crea un cliente de Google Cloud Storage usando la clave de la cuenta de servicio
# client = storage.Client.from_service_account_json(key_path)

# # Obtén el blob del archivo Parquet
# bucket = client.get_bucket(bucket_name)

# #------------------------------------------------------------------------------------------------------------------
# # # Lista los objetos en el bucket
# # blobs = list(bucket.list_blobs())

# # # Imprime los nombres de los objetos
# # for blob in blobs:
# #     print(blob.name)

# #------------------------------------------------------------------------------------------------------------------
# # # Leo un parquet en particular
# # blob = bucket.blob(objet_name_read)

# # # Descarga el archivo Parquet localmente
# # blob.download_to_filename(local_filename)

# # # Lee el archivo Parquet usando pyarrow
# table = pq.read_table(local_filename)

# # # Convierte la tabla de pyarrow a un DataFrame de pandas si es necesario
# df = table.to_pandas()

# #Imprimo el esquema
# print(pq.read_schema(local_filename))
# print(df.dtypes)

# #Imprimo el contenido
# print(df.head())

# #------------------------------------------------------------------------------------------------------------------

# # #bajo el df pandas a parquet
# # df.to_parquet(local_filename + '_up_part')

# # #blob = bucket.blob(objet_name_read + '_up')
# # #blob.upload_from_filename(local_filename + '_up')

# # #bajo el df pandas a parquet, particionado
# # df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date

# # table = pa.Table.from_pandas(df)

# # pq.write_to_dataset(
# #     table,
# #     root_path='archivo.parquet_up_part',
# #     partition_cols=['lpep_pickup_date']
# # )
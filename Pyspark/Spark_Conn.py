########################################################################################################
# Diferentes formas de conectar a Spark
########################################################################################################

from time import sleep
from pyspark.sql import SparkSession
from pyspark import SparkConf

conf = SparkConf().setAppName("PysparkPruebas") \
           .setMaster("local[*]") \
           .set("spark.sql.debug.maxToStringFields", 1000) \
           .set("spark.sql.catalogImplementation", "hive") \
           .set("spark.driver.memory", "2g") \
           .set("spark.executor.memory", "2g") 

spark = SparkSession.builder \
        .config(conf=conf) \
        .getOrCreate()

sc = spark.sparkContext
#spark.sparkContext.setLogLevel("INFO")

print('SaprkVer: ' + sc.version)
print('PythonVer: ' + sc.pythonVer)
print('PythonVer: ' + sc.master)

df = spark.read \
    .option("header", "true") \
    .option("sep", ";") \
    .csv('/home/julian/workspaces/prueba-python/datasources/shanghai-world-university-ranking.csv')

df.show()

#poniendo breack acá puedo ver el history server: http://localhost:4040/jobs/
sleep(1)

# #########################################################################################################
# #########################################################################################################
# # Revisión de problemas con pandas
# #########################################################################################################

# # Importa las bibliotecas necesarias
# import pandas as pd
# from pyspark.sql import SparkSession

# #workaround por incompatibilidad de versione sde pandas y spark!
# pd.DataFrame.iteritems = pd.DataFrame.items

# # Inicializa una sesión de Spark
# spark = SparkSession.builder \
#     .appName("Python Spark DataFrame Example") \
#     .getOrCreate()

# # Crea un DataFrame de Pandas de ejemplo
# pandas_df = pd.DataFrame({
#     'name': ['Alice', 'Bob', 'Charlie'],
#     'age': [30, 25, 35]
# })

# # Imprime el DataFrame de Pandas para verificar
# print("DataFrame de Pandas:")

# # Convierte el DataFrame de Pandas a un DataFrame de Spark
# df = spark.createDataFrame(pandas_df)

# # Muestra el DataFrame de Spark
# df.show()
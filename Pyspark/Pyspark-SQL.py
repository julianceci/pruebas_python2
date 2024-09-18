import sys, time
import matplotlib.pyplot as plt
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col
from pyspark.sql.window import Window
from pyspark.sql.types import *

conf = SparkConf().setAppName("PysparkPruebas") \
           .setMaster("local[*]") \
           .set("spark.sql.debug.maxToStringFields", 1000) \
           .set("spark.sql.catalogImplementation", "hive") \
           .set("spark.sql.warehouse.dir", "file:///home/julian//Documents/prueba-python/spark-warehouse")
#           .set("spark.executor.memory", "2g") 

# Crear una sesión de Spark
spark = SparkSession.builder \
      .config(conf=conf) \
      .getOrCreate()

sc = spark.sparkContext

#spark.sparkContext.setLogLevel("INFO")

print('SaprkVer: ' + sc.version)
print('PythonVer: ' + sc.pythonVer)
print('PythonVer: ' + sc.master)

##########################################################################################################
##########################################################################################################


##########################################################################################################
#Uso de Hive para definir tablas con parquet

spark.sql("CREATE DATABASE IF NOT EXISTS my_database")
spark.sql("USE my_database")

print(spark.catalog.listTables())
##########################################################################################################
sys.exit()

file_path = "file:///home/julian//Documents/prueba-python/datasources/targets/part-*"

parquet_targets = (spark.read.parquet(file_path)
                   .select("id", "approvedSymbol", "biotype", "transcriptIds", "canonicalExons")
      )

df = (parquet_targets
      .withColumn("transcriptId", F.explode(parquet_targets.transcriptIds))
      .select("id", "approvedSymbol", "biotype", "transcriptId", "canonicalExons")
      )

# Guardar el DataFrame como tabla Hive en formato Parquet...
df.write.mode("overwrite").partitionBy("biotype").saveAsTable("my_database.targets_tbl")
#df.write.mode("overwrite").saveAsTable("my_database.targets_tbl")

resutSQL = spark.sql('''SELECT biotype, count(1) as count 
                          FROM my_database.targets_tbl
                         GROUP BY biotype 
                         ORDER BY count DESC''')

resutDSL = df.groupBy(col("biotype")).count().orderBy(col("count").desc())

spark.sql("SHOW TABLES").show()
resutDSL.show(10)
resutSQL.show(10)

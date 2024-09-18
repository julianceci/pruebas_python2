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
           .set("spark.sql.debug.maxToStringFields", 1000) 
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
#JSON
synonyms_schema = ArrayType(
      StructType([
            StructField('label', StringType(), True),
            StructField('source', StringType(), True)
      ])
)

file_path = "file:///home/julian//Documents/prueba-python/datasources/targets_JSON/part-*.json"

df = (spark.read.json(file_path)
                   .select("id", "biotype", "canonicalTranscript", "transcriptIds", "synonyms")
      )

#df = df.withColumn("col_struct", F.from_json(df["synonyms"], synonyms_schema))
df.printSchema()
df.show(1)

##########################################################################################################
sys.exit()

##########################################################################################################
#Parquet
file_path = "file:///home/julian//Documents/prueba-python/datasources/targets_parquet/part-*.parquet"

df = (spark.read.parquet(file_path)
                   .select("id", "biotype", "canonicalTranscript", "transcriptIds", "synonyms")
      )

df = df.withColumn("id_canonicalTR", df["canonicalTranscript.id"])
df = df.withColumn("transcriptIds_item1", col("transcriptIds").cast("array<string>").getItem(0).alias("primer_elemento"))
df = df.withColumn("cant_transcriptIds", F.size(col("transcriptIds")))
df = df.withColumn("synonyms_item1", col("synonyms")[0])

df.printSchema()
df.show(1)
df.select(["synonyms.source"]).limit(1).show(truncate=False)
df.withColumn("synonyms_list", F.explode(df.synonyms)).select("synonyms_list").show(truncate=False)


##########################################################################################################
sys.exit()

df = (df
      .withColumn("transcriptId", F.explode(df.transcriptIds))
      .select("id", "approvedSymbol", "biotype", "transcriptId")
      )

#add df as a table in the spark session
df.createOrReplaceTempView("targest_table")

resutSQL = spark.sql('''SELECT biotype, count(1) as count 
                          FROM targest_table 
                         GROUP BY biotype 
                         ORDER BY count DESC''')

resutDSL = df.groupBy(col("biotype")).count().orderBy(col("count").desc())

resutSQL.show(10)
resutDSL.show(10)

##########################################################################################################

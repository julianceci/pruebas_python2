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
#Invento de un caso integral....
def contarItems(arrayParam):
      return len(arrayParam)

udf_contarItems = F.udf(contarItems, IntegerType())

file_path = "file:///home/julian//Documents/prueba-python/datasources/targets/part-00000-*"

parquet_targets = (spark.read.parquet(file_path)
                   .select("id", "approvedSymbol", "biotype", "transcriptIds", "canonicalExons")
      )

df = (parquet_targets
#      .withColumn("transcriptId", F.explode(parquet_targets.transcriptIds))
      .select("id", "approvedSymbol", "transcriptIds", "biotype"
              ,F.when(col("approvedSymbol")=="CD99", "CHECK_CD99").otherwise("UN_CHECK_CD99").alias("CHECK_CD99")
              ,F.monotonically_increasing_id().alias("ID_SPARK")
              ,F.split(col("biotype"), '_').alias("Prueba Split")
              ,F.size(col("transcriptIds")).alias("cant TR")
              ,udf_contarItems(col("transcriptIds")).alias("cant TR UDF")
      )
      .filter(col("cant TR")<=3)
      .orderBy("biotype", col("cant TR").desc())
      )
#df.show()
df.explain()

window_spec = Window.partitionBy("biotype").orderBy(col("cant TR").desc())
window_spec_2 = Window.partitionBy("biotype").orderBy(col("rank"))
ranked_df = (df
            .withColumn("rank", F.row_number().over(window_spec))
#            .withColumn("rank()", F.rank().over(window_spec))
#            .withColumn("lag", F.lag("ID_SPARK").over(window_spec))
#            .withColumn("lead", F.lead("ID_SPARK").over(window_spec))
            .withColumn("lista_inc", F.collect_list(col("ID_SPARK")).over(window_spec_2))
#            .withColumn("first", F.first(col("ID_SPARK")).over(window_spec))
            .withColumn("match", F.when(F.array_contains(F.collect_list(col("ID_SPARK")).over(window_spec), 287), "1"))
            .withColumn("Id_biotype", F.first(col("ID_SPARK")).over(window_spec_2))
)
#ranked_df = ranked_df.filter("rank = 1")
#ranked_df.show()
#ranked_df.explain()

#resutDSL.explain()
#df.groupBy(col("biotype")).agg(F.count('*').alias("cnt"), F.countDistinct("Prueba Split").alias("cnt_dct")).orderBy(col("cnt").desc()).show()
#df.groupBy("biotype").sum("cant TR", "ID_SPARK").show()

##########################################################################################################
sys.exit()

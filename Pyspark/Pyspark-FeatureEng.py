import sys, time

import seaborn as sns
import matplotlib.pyplot as plt

from pyspark.sql import functions as F
from pyspark.sql.functions import col
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.types import *
from pyspark.sql.window import Window
import pandas as pd
import numpy as np

conf = SparkConf().setAppName("PysparkPruebas") \
           .setMaster("local[*]") \
           .set("spark.sql.debug.maxToStringFields", 1000) 
#           .set("spark.executor.memory", "2g") 

# Crear una sesión de Spark
spark = SparkSession.builder \
      .config(conf=conf) \
      .getOrCreate()

SWUR_schema = StructType([
  # Define a StructField for each field
  StructField('World rank', StringType(), True),
  StructField('University', StringType(), True),
  StructField('National rank', StringType(), True),
  StructField('Total score', DoubleType(), nullable=False),
  StructField('Alumni', DoubleType(), True),
  StructField('Award', DoubleType(), True),
  StructField('Hi Ci', DoubleType(), True),
  StructField('N&S', DoubleType(), True),
  StructField('PUB', DoubleType(), True),
  StructField('PCP', DoubleType(), True),
  StructField('Year', StringType(), True),
  StructField('World rank integer', IntegerType(), True),
  StructField('Country', StringType(), True)
])

##########################################################################################################
#jugando con fechas que es un clásico...

# Define la fecha de inicio y fin
fecha_inicio = "2020-01-01"
fecha_fin = "2023-01-01"

sec_dates = pd.date_range(start=fecha_inicio, periods=10)
rnd_dates = np.random.choice(pd.date_range(start=fecha_inicio, end=fecha_fin, freq='T'), size=10, replace=True)

# Crea un DataFrame de Pandas con fechas
pandas_df = pd.DataFrame({
    'sec_dates': sec_dates,
    'rnd_dates': rnd_dates
})

# Convierte el DataFrame de Pandas a un DataFrame de PySpark
df = spark.createDataFrame(pandas_df)
windows_spec = Window.partitionBy().orderBy('sec_dates')

df = (df
      .withColumn('Year', F.year(df.sec_dates))
      .withColumn('Month', F.month(df.sec_dates))
      .withColumn('Dayofmonth', F.dayofmonth(df.sec_dates))
      .withColumn('Datediff', F.datediff(df.rnd_dates, df.sec_dates))
      .withColumn('lag_sec_dates', F.lag('sec_dates').over(windows_spec))
      #jugar con las clásicas diferencias horarias e intervalos de tiempo raros.... SQL y SPARK
)

# Muestra el DataFrame resultante
# df.show()

##########################################################################################################
# sys.exit()

##########################################################################################################
##########################################################################################################

file_path = "file:///home/julian//Documents/prueba-python/datasources/shanghai-world-university-ranking.csv"
#df = spark.read.csv(file_path, header=True, inferSchema=True, sep=";")
##########################################################################################################
#uso de esquema en la lectura, uso de cast para un supuesta integuer
df = spark.read.csv(file_path, header=True, schema=SWUR_schema, sep=";")
#df.printSchema()
df = df.select(col('World rank').cast('integer').alias('WorldRank'), 'University', 'Country', 'Year', 'Total score', 'PUB', 'PCP', (col('PUB')*col('PCP')).alias('calc'))
#df.show(10)

##########################################################################################################
#...

##########################################################################################################
# sys.exit()

##########################################################################################################
#reemplazo de valor nulo
#df.fillna({'Total score': 666}).show(10)
#df.fillna('666', subset=['Total score']).show(10) #Esto NO ANDA!!!!!!
#El withColumn con un nombre que ya esta en el dataframe lo pisa directo! 
#df.withColumn('Total score', F.when(F.isnull(col('Total score')), 666).otherwise(col('Total score'))).show(10)

#filtrado de valores/filas nulas
#df.filter(~F.isnull(col('Total score'))).show(10)
#df.dropna(how='all', subset=['Total score']).show(10)

##########################################################################################################
#drop con lista y filtrado algo complejo
drop_cols = ['PUB', 'PCP']
sample_df = df.drop(*drop_cols)
sample_df = sample_df.filter(~F.upper(sample_df['University']).like('%COLLEGE%') & sample_df['University'].startswith('University'))

worldRank_filtro = [70,72]
sample_df = sample_df.withColumn('worldRank_filtro', F.when(sample_df['WorldRank'].isin(worldRank_filtro) | sample_df['WorldRank'].isNull(), 'CHK'))
sample_df = sample_df.withColumn('split_Univ', F.split(sample_df['University'], ' ').getItem(0))
sample_df.show(10)

##########################################################################################################
sys.exit()


##########################################################################################################
#Limpio los outliers
std_val = sample_df.agg({'calc': 'stddev'}).collect()[0][0]
mean_val = sample_df.agg({'calc': 'mean'}).collect()[0][0]

hi_bound = mean_val + (3*std_val)
lo_bound = mean_val - (3*std_val)

sample_df = sample_df.filter((sample_df['calc'] < hi_bound)  & (sample_df['calc'] > lo_bound))
sample_df.orderBy(col('calc').desc()).show(truncate=False)
print(hi_bound, lo_bound)


#sample_df = df.select(['calc', 'PCP']).sample(False, 0.5, 42)
#pandas_df = sample_df.toPandas()

#sns.lmplot(x="PCP", y="calc", data=pandas_df)
#plt.show()

#sns.displot(pandas_df["calc"], color="r", label="Actual Value")
#plt.show()

##########################################################################################################
sys.exit()


file_path = "file:///home/julian//Documents/prueba-python/datasources/targets/part-00000-*"

parquet_targets = (spark.read.parquet(file_path)
                   .select("id", "approvedSymbol", "biotype", "transcriptIds", "canonicalExons", F.size(col("canonicalExons")).alias("Cant_CE"))
      )

print(parquet_targets.dtypes)
print('# de columnas: {}'.format(len(parquet_targets.columns)))
#parquet_targets_10 = parquet_targets.limit(10)
parquet_targets_sample = parquet_targets.sample(False, 0.5, 42)

print('# de filas df original: ' + str(parquet_targets.count()))
parquet_targets.limit(1).show(10, truncate=False)
print('# de filas df smpleado: ' + str(parquet_targets_sample.count()))
parquet_targets_sample.show(10)

#Paso a Pandas para graficar
pandas_df = parquet_targets_sample.toPandas()
sns.displot(pandas_df["Cant_CE"], color="r", label="Actual Value")
plt.show()

##########################################################################################################
sys.exit()

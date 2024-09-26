import sys
import matplotlib.pyplot as plt
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col
from pyspark.sql.window import Window

conf = SparkConf().setAppName("PysparkPruebas") \
           .setMaster("local[*]") \
           .set("spark.sql.debug.maxToStringFields", 1000) \
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


file_path = "file:///home/julian//Documents/prueba-python/datasources/world all university rank and rank score.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

df_pandas = df.select("rank", "ranking-institution-title", "location", "Overall scores").toPandas().head(10)

#plt.clf()

#Horizantal Bar ########################################################################################################
df_pandas.plot(kind='barh', x='ranking-institution-title', y='rank', colormap='winter_r')
plt.show()

##########################################################################################################
sys.exit()

#Histogram ########################################################################################################
plt.hist(df_pandas["rank"], bins=5, edgecolor='black')

# Agregar etiquetas
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.title('Histograma')

# Mostrar el histograma
plt.show()


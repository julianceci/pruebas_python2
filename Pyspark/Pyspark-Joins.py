from pyspark.sql import SparkSession
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast

spark = SparkSession.builder.appName("Ejemplo").getOrCreate()

# Crear DataFrames de ejemplo
data1 = [(1, "A"), (2, "B"), (3, "C")]
data2 = [(1, "X"), (3, "Y")]

columns = ["ID", "Value"]
df1 = spark.createDataFrame(data1, columns)
df2 = spark.createDataFrame(data2, columns)

# Realizar la operación EXISTS
#result = df1.join(df2, df1.ID == df2.ID, "left_semi")

# Realizar la operación NOT EXISTS
#result = df1.join(df2, df1.ID == df2.ID, "left_anti")

# Agrego datos de tabla dimensión, poniendo solo el "ID" (campo en comun), el join no duplica la columna.
#result = df1.join(broadcast(df2.withColumnRenamed("Value", "Value_dim")), df1.ID == df2.ID, 'left')
#result = df1.join(broadcast(df2.withColumnRenamed("Value", "Value_dim")), "ID", 'left')

#Unión de dataframes
result = df1.union(df2)

result.show()

##########################################################################################################
sys.exit()

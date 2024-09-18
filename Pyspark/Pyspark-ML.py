import sys
import matplotlib.pyplot as plt
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col
from pyspark.sql.window import Window

# Import the library for ALS
from pyspark.mllib.recommendation import ALS, Rating
# Import the library for Logistic Regression
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
# Import the library for Kmeans
from pyspark.mllib.clustering import KMeans


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


file_path = "file:///home/julian//Documents/prueba-python/datasources/ml-100k/u.data"

data = sc.textFile(file_path)

###########################################################################################
#Collaborative filtering
###########################################################################################
# Loading Movie Lens dataser into RDD 

# Split the RDD 
ratings = data.map(lambda l: l.split('\t'))

# Transform the ratings RDD 
ratings_final = ratings.map(lambda line: Rating(int(line[0]), int(line[1]), float(line[2])))

# Split the data into training and test
training_data, test_data = ratings_final.randomSplit([0.8, 0.2])


###########################################################################################
# Model training and predictions - ALS (Alternating Least Squares)

# Create the ALS model on the training data
model = ALS.train(training_data, rank=10, iterations=10)

# Drop the ratings column 
testdata_no_rating = test_data.map(lambda p: (p[0], p[1]))

# Predict the model  
predictions = model.predictAll(testdata_no_rating)

# Return the first 2 rows of the RDD
print(predictions.take(2))


###########################################################################################
# Model evaluation using MSE (Mean Square Error) - (original rating – predicted rating)**2

# Prepare ratings data
rates = ratings_final.map(lambda r: ((r[0], r[1]), r[2]))

# Prepare predictions data
preds = predictions.map(lambda r: ((r[0], r[1]), r[2]))

# Join the ratings data with predictions data
rates_and_preds = rates.join(preds)

# Calculate and print MSE
MSE = rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Mean Squared Error of the model for the test data = {:.2f}".format(MSE))



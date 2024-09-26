import sys
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col, avg, lit
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

##########################################################################################################

# Datos de entrada
courses_data = [(21, "CourseSQL1", "SQL"), (22, "CourseSQL2", "SQL"), (23, "CourseSQL3", "SQL"), (24, "CourseSQL4", "SQL"), (25, "CourseSQL5", "SQL"),
                (31, "CourseR1", "R"), (32, "CourseR2", "R"), (33, "CourseR3", "R"), (34, "CourseR4", "R"),
                (41, "CoursePY1", "PYTHON"), (42, "CoursePY2", "PYTHON"),
                (51, "CoursePBI1", "POWERBI")
                ]
courses_columns = ["course_id", "title", "programming_language"]
courses_df = spark.createDataFrame(courses_data, courses_columns)

course_ratings_data = [(1, 24, 33.8), (1, 25, 31.1), (1, 31, 1.8), 
                       (2, 25, 2.88), (2, 33, 2.1), (2, 41, 12.8), (2, 42, 6.2),
                       (3, 33, 3.8), (3, 34, 10.7),
                       (4, 23, 7.8), (4, 32, 10.7), (4, 41, 11.7)
                       ]
course_ratings_columns = ["user_id", "course_id", "rating"]
course_ratings_df = spark.createDataFrame(course_ratings_data, course_ratings_columns)


def avg_course_ratings_data_trf(course_ratings):
      avg_course_ratings_data_df = course_ratings.groupBy("course_id").agg(avg("rating").alias("rating"))
      return avg_course_ratings_data_df

def courses_to_recommend_data_trf(course_ratings, courses):

      course_ratings_PL = course_ratings.join(courses.select("course_id", "programming_language"), course_ratings.course_id == courses.course_id, "left")
      user_course_PL_cant = course_ratings_PL.groupBy("user_id", "programming_language").count().withColumnRenamed("count", "cant_courses")
      
      window_spec = Window.partitionBy("user_id").orderBy(f.col("cant_courses").desc())
      ranked_df = user_course_PL_cant.withColumn("rank", f.row_number().over(window_spec))
      ranked_filter_df = ranked_df.filter("rank = 1")

      courses_to_recommend_all = ranked_filter_df.join(courses_df, ranked_filter_df.programming_language == courses_df.programming_language, "left").select("user_id", "course_id")
      
      courses_to_recommend_all = courses_to_recommend_all.join(course_ratings_df,
                                          (courses_to_recommend_all["user_id"] == course_ratings_df["user_id"]) & 
                                          (courses_to_recommend_all["course_id"] == course_ratings_df["course_id"]),
                                           "anti")

      courses_to_recommend_data_df = courses_to_recommend_all
      return courses_to_recommend_data_df


# Función de transformación
def transform_recommendations(avg_course_ratings, courses_to_recommend):
    # Unir ambos DataFrames
    merged = courses_to_recommend.join(avg_course_ratings, "course_id", "left").fillna({"rating": 1})
   
    # Calcular el ranking dentro de cada grupo de usuario
    window_spec = Window.partitionBy("user_id").orderBy(f.col("rating").desc())
    ranked_df = merged.withColumn("rank", f.row_number().over(window_spec))
    
    # Seleccionar las principales recomendaciones (en este caso, las 2 mejores)
    recommendations = ranked_df.filter("rank <= 2").select("user_id", "course_id", "rating")
    
    return recommendations

# Utilizar la función con los DataFrames definidos
recommendations = transform_recommendations(avg_course_ratings_data_trf(course_ratings_df), courses_to_recommend_data_trf(course_ratings_df, courses_df))
recommendations.show()

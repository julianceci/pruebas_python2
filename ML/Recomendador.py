from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsRegressor

import numpy as np
import joblib

#-----------------------------------------------------------------------------------------------
# Ejemplo usando usuario-ítem manual------------------------------------------------------------

# Supón que tienes una matriz de usuario-ítem
user_item_matrix = np.array([
    [5, 3, 0],
    [4, 0, 5],
    [0, 2, 4],
    [4, 2, 0],
    [2, 2, 10],
    [1, 1, 1]
])

def show_similarity():
    #-------------------------------------------------------
    # Calcula la similaridad entre los usuarios
    user_similarity = cosine_similarity(user_item_matrix)
    print(user_similarity)


def show_knn_manual():
    #-------------------------------------------------------
    # Creamos el modelo k-NN
    knn = NearestNeighbors(metric='cosine', algorithm='brute')

    # Ajustamos el modelo a la matriz de usuarios e ítems
    knn.fit(user_item_matrix)

    # Obtenemos los vecinos más cercanos para un usuario en particular (por ejemplo, el usuario 0)
    nuevo_usuario_pelicula = [[0, 1, 7]]  # Calificaciones dadas por el nuevo usuario a algunas películas
    distances, indices = knn.kneighbors(nuevo_usuario_pelicula, n_neighbors=4)

    print(f"Índices de los vecinos más cercanos: {indices}")
    print(f"Distancias a los vecinos más cercanos: {distances}")


    # Vamos a predecir la calificación del nuevo usuario para la pelicula 1 (la que no vió)
    pelicula_a_predecir = 0

    # Tomamos las calificaciones de los vecinos para la película 1
    calificaciones_vecinos = user_item_matrix[indices[0], pelicula_a_predecir]

    # Similaridades son 1 - distancias, ya que las distancias menores indican mayor similaridad
    similaridades = 1 - distances[0]

    # Predicción ponderada
    prediccion = np.dot(calificaciones_vecinos, similaridades) / np.sum(similaridades)

    print(f"Predicción de Usuario nuevo para la Película 1: {prediccion}")

    # Guardar el modelo en un archivo
    #joblib.dump(knn, 'modelo_entrenado.pkl')

    #Para cargar el modelo guardado en cualquier otro momento
    #modelo_cargado = joblib.load('modelo_entrenado.pkl')


def show_knn_movieLens():
    #-----------------------------------------------------------------------------------------------
    # Ejemplo usando MovieLens ---------------------------------------------------------------------

    # Cargar los datos
    data = Dataset.load_builtin('ml-100k') 

    # Dividimos los datos en conjunto de entrenamiento y prueba
    trainset, testset = train_test_split(data, test_size=0.25)

    # Usamos SVD (descomposición de valores singulares) para el modelo
    model = SVD()
    model.fit(trainset)

    # Hacemos predicciones en el conjunto de prueba
    predictions = model.test(testset)

    # Evaluamos el modelo
    accuracy.rmse(predictions)

    # Obtener el conjunto de datos de entrenamiento
    trainset = data.build_full_trainset()

    # Imprimir las calificaciones (user, item, rating) del trainset
    for uid, iid, rating in trainset.all_ratings():
        print(f"User: {trainset.to_raw_uid(uid)}, Item: {trainset.to_raw_iid(iid)}, Rating: {rating}")


#-----------------------------------------------------------------------------------------------
# show_similarity()
show_knn_manual()
#show_knn_movieLens()

#Ejemplo: Agrupación de clientes según el comportamiento de compra

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Generar datos simulados con 4 centros
X, _ = make_blobs(n_samples=300, centers=4, random_state=0, cluster_std=0.60)

# Crear el modelo K-Means y ajustarlo a los datos
kmeans = KMeans(n_clusters=4)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

# Visualizar los puntos de datos con los clusters
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

# Visualizar los centroides
centroides = kmeans.cluster_centers_
plt.scatter(centroides[:, 0], centroides[:, 1], c='red', s=200, alpha=0.75, marker='X')

plt.title('Agrupación K-Means')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.show()

# Mostrar las coordenadas de los centroides
print("Coordenadas de los centroides:", centroides)


# Interpretación:
# -Puntos coloreados: Representan los datos asignados a diferentes clusters.
# -Centroides: Son los puntos centrales de cada cluster, y el algoritmo ajusta su posición para minimizar la distancia entre los puntos del cluster y el centroide.
# -Este algoritmo es útil para descubrir patrones o estructuras en los datos sin etiquetas.

# Explicación del código:
# 1-Datos simulados: Utilizamos make_blobs para generar un conjunto de datos sintético con 4 grupos (centros) y 300 puntos.
# 2-K-Means: Definimos el número de clusters como 4 y aplicamos el algoritmo K-Means para agrupar los puntos en 4 clusters.

# Visualización:
# -Los puntos de colores representan los diferentes clusters encontrados por K-Means.
# -Los X rojos son los centroides, es decir, el punto central de cada cluster.
# -Centroides: Imprimimos las coordenadas de los centroides para ver dónde se han localizado después del ajuste.
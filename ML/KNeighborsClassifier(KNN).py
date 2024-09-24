#Ejemplo: Clasificar puntos en función de sus vecinos más cercanos.

from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

# Generar datos
X, y = make_blobs(n_samples=100, centers=2, random_state=0, cluster_std=1)

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Modelo KNN
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# Predicciones
predicciones = model.predict(X_test)

# Mostrar los valores predichos junto con los reales
for real, pred in zip(y_test, predicciones):
    print(f'Real: {real}, Predicho: {pred}')

# Visualización
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', s=50)
plt.scatter(X_test[:, 0], X_test[:, 1], c=predicciones, s=100, marker='X')  # Datos de prueba
plt.title('K-Nearest Neighbors')
plt.show()

#Ejemplo: Clasificación de puntos en un plano.

from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import matplotlib.pyplot as plt

# Generar datos
X, y = make_blobs(n_samples=100, centers=2, random_state=0, cluster_std=1)

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Modelo SVM
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Predicciones
predicciones = model.predict(X_test)

# Mostrar los valores predichos junto con los reales
for real, pred in zip(y_test, predicciones):
    print(f'Real: {real}, Predicho: {pred}')

# Visualización
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', s=50)
plt.scatter(X_test[:, 0], X_test[:, 1], c=predicciones, s=100, marker='X')  # Datos de prueba
plt.title('SVM')
plt.show()


# Interpretación:
# -Puntos azules y rojos: Los datos de entrenamiento están representados por puntos en el gráfico. Los colores azul y rojo representan las dos clases que intentamos separar.
# -X negras: Representan los puntos de prueba (test set), sobre los que el modelo hace predicciones.
# -Línea divisoria (si se muestra): Esta es la frontera de decisión que el modelo crea para separar las dos clases.

# Interpretación de los resultados:
# -Los puntos azules y rojos son los datos originales.
# -Los "X" negras representan los datos de prueba (test set) clasificados por el modelo.
# -Real vs Predicho: El código imprimirá los resultados de las predicciones, para que veas si el modelo clasificó correctamente o no.

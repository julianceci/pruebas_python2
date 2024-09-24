#Ejemplo: Clasificar puntos en función de sus vecinos más cercanos.

from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Cargar el conjunto de datos MNIST
mnist = fetch_openml('mnist_784')
X = mnist.data
y = mnist.target.astype('int')

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Modelo de red neuronal
model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=20)
model.fit(X_train, y_train)

# Predicciones
predicciones = model.predict(X_test)

# Mostrar algunos valores reales y predichos
for real, pred in zip(y_test[:10], predicciones[:10]):
    print(f'Real: {real}, Predicho: {pred}')

# Precisión del modelo
accuracy = accuracy_score(y_test, predicciones)
print(f'Precisión: {accuracy:.2f}')

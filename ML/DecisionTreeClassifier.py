#Ejemplo: Clasificar especies de flores.

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree
import matplotlib.pyplot as plt

# Usando el conjunto de datos Iris
data = load_iris()
X = data.data
y = data.target

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Modelo de árbol de decisión
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Predicciones
predicciones = model.predict(X_test)

# Mostrar los valores predichos junto con los reales
for real, pred in zip(y_test, predicciones):
    print(f'Real: {real}, Predicho: {pred}')

# Precisión del modelo
accuracy = accuracy_score(y_test, predicciones)
print(f'Precisión: {accuracy:.2f}')

# Visualización del árbol
plt.figure(figsize=(10, 8))
tree.plot_tree(model, filled=True)
plt.show()

#Ejemplo: Decidir si una flor es de clase A o B

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Usando el conjunto de datos Iris para clasificación
data = load_iris()
X = data.data[data.target != 2]  # Solo tomamos 2 clases
y = data.target[data.target != 2]

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Modelo de regresión logística
model = LogisticRegression()
model.fit(X_train, y_train)

# Predicciones
predicciones = model.predict(X_test)

# Mostrar resultados de las predicciones
for real, pred in zip(y_test, predicciones):
    print(f'Real: {real}, Predicho: {pred}')

# Precisión del modelo
accuracy = accuracy_score(y_test, predicciones)
print(f'Precisión: {accuracy:.2f}')

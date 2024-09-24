#Ejemplo: Clasificación de la calidad del vino

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Cargar el conjunto de datos de vino
data = load_wine()
X = data.data
y = data.target

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Modelo de bosque aleatorio
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Predicciones
predicciones = model.predict(X_test)

# Mostrar algunos valores reales y predichos
for real, pred in zip(y_test[:10], predicciones[:10]):
    print(f'Real: {real}, Predicho: {pred}')

# Precisión del modelo
accuracy = accuracy_score(y_test, predicciones)
print(f'Precisión: {accuracy:.2f}')

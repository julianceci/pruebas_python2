#Ejemplo: Predecir el precio de una casa en función de su tamaño.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Simulando algunos datos
data = {
    'tamaño': [1500, 1600, 1700, 1800, 1900, 2000],
    'precio': [300000, 320000, 340000, 360000, 380000, 400000]
}
df = pd.DataFrame(data)

# Dividir los datos
X = df[['tamaño']]
y = df['precio']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Predicciones
predicciones = model.predict(X_test)

# Mostrar los valores predichos junto con los reales
for real, pred in zip(y_test, predicciones):
    print(f'Real: {real}, Predicho: {pred:.2f}')

# Visualización
plt.scatter(X, y, color='blue')
plt.plot(X_test, predicciones, color='red')
plt.title('Regresión Lineal')
plt.xlabel('Tamaño (pies cuadrados)')
plt.ylabel('Precio ($)')
plt.show()

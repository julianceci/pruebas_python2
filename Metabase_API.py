# #Para obtener el token id ejecutar desde línea de comando:
# curl -X POST \
# -H "Content-Type: application/json" \
# -d '{"username": "julianceci@gmail.com", "password": "metabase77"}' \
# http://localhost:3000/api/session

# #Devuelve el token ID: {"id":"07d0a8ca-4703-4064-9876-18a884e1ac5a"}

# #Por ejemplo con: http://localhost:3000/question/33-sql-radar-api
# #Usamos el id de la pregunta: 33-pregunta-sql

# #Para ejecutar la consulta API en este caso
# curl -X POST \
# -H "Content-Type: application/json" \
# -H "X-Metabase-Session: 07d0a8ca-4703-4064-9876-18a884e1ac5a" \
# http://localhost:3000/api/card/33/query/json

##Va lo mismo pero desde python

import requests
import pandas as pd
import plotly.express as px

# Configura tus credenciales de Metabase y el ID de la consulta
username = "julianceci@gmail.com"
password = "metabase77"
metabase_url = "http://localhost:3000"
question_id = 33  # ID de la pregunta

# Autenticarse en Metabase
auth_response = requests.post(
    f"{metabase_url}/api/session",
    json={"username": username, "password": password}
)
token = auth_response.json()["id"]

# Obtener los datos de la pregunta
headers = {"X-Metabase-Session": token}
data_response = requests.post(
    f"{metabase_url}/api/card/{question_id}/query/json",
    headers=headers
)

# Cargar los datos en un DataFrame de pandas
data = data_response.json()
df = pd.DataFrame(data)

# Configura el gráfico de araña (ajusta las columnas según tu dataset)
categories = df['User_SOURCE']  # Columna de categorías (eje angular)
values = df.iloc[:, 1:]      # Otras columnas con valores (eje radial)

# Generar gráfico de araña
fig = px.line_polar(df, r=values.values.flatten(), theta=categories.repeat(values.shape[1]), line_close=True)
fig.show()

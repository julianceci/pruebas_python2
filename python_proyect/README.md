# My Package

Descripción del paquete.

## Instalación

Puedes instalar este paquete usando:

## Activación de entorno virtula de python
- python3 -m venv venv #creación
- source venv/bin/activate #activación
- deactivate

- pip show nombre_paquete #para ver la versión entre otras csoas
- pip freeze > requirements.txt #carga el requirements.txt con cada programa y su version!
- pip install -r requirements.txt #Instalamos las dependencias para el entorno de trabajo

## Referencias a mi paquete
export PYTHONPATH=$(pwd) #desde la raíz del proyecto para que encuentro los paquetes
echo $PYTHONPATH #para chequear valor
unset PYTHONPATH



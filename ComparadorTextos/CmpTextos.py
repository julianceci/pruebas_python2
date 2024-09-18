"""
# Pruebas de comparación de texto-------------------------------------------------------------------------------------------
"""

import difflib

#texto1 = '''...'''
#texto2 = '''...'''

# Lee el contenido de los archivos
with open("Texto1.txt", "r") as f:
    texto1 = f.read()

with open("Texto2.txt", "r") as f:
    texto2 = f.read()


# Separa los textos en líneas
lineas1 = texto1.splitlines()
lineas2 = texto2.splitlines()

# Crea un objeto Differ
d = difflib.Differ()

# Encuentra las diferencias entre las líneas
resultado = list(d.compare(lineas1, lineas2))

# Imprime el resultado
print("\n".join(resultado))

# Guarda el resultado en un archivo de texto
with open("resultado.txt", "w") as f:
    f.write("\n".join(resultado))
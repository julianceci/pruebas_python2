import sys, time, textwrap, contextlib
import numpy as np
import pandas as pd

#sys.exit()
##########################################################################################################

#--------------------------------------------------------------------------------------------------
#Decorators
def print_return_type(func):
  # Define wrapper(), the decorated function
  def wrapper(*args, **kwargs):
    # Call the function being decorated
    result = func(*args, **kwargs)
    print('{}() returned type {}'.format(
      func.__name__, type(result)
    ))
    return result
  # Return the decorated function
  return wrapper
  
@print_return_type
def foo(value):
  return value

# print(foo(42))
# print(foo([1, 2, 3]))
# print(foo({'a': 42}))

#--------------------------------------------------------------------------------------------------
#context manager

#Sin context manager --------------------
archivo_path = "archivo.txt"
try:
  archivo = open(archivo_path, 'r')
  # Trabajas con el archivo
  contenido = archivo.read()
  print(contenido)
except FileNotFoundError:
  print(f"El archivo {archivo_path} no existe.")
finally:
  # Cierra el archivo solo si se abrió
  try:
    archivo.close()
  except NameError:
    pass  # Si 'archivo' no fue definido, no hacemos nada

#Con context manager --------------------
#Ejemplo 1: Leer un archivo línea por línea
try:
  with open('archivo.txt', 'r') as archivo:
      for linea in archivo:
          print(linea.strip())  # Usar strip() para eliminar espacios o saltos de línea extra
except FileNotFoundError:
    print("Error: El archivo no fue encontrado.")
except IOError:
    print("Error: Ocurrió un problema al leer el archivo.")
except Exception as e:
    print(f"Se produjo un error inesperado: {e}")

# #Ejemplo 2: Leer todo el contenido del archivo de una sola vez
# with open('archivo.txt', 'r') as archivo:
#     contenido = archivo.read()
#     print(contenido)

# #Ejemplo 3: Leer el archivo en una lista, donde cada línea es un elemento de la lista
# with open('archivo.txt', 'r') as archivo:
#     lineas = archivo.readlines()  # Cada línea será un elemento de la lista
#     print(lineas)

# #Ejemplo 4: Escribir en un archivo
# with open('archivo.txt', 'w') as archivo:
#     archivo.write('Esta es una nueva línea de texto.\n')
#     archivo.write('Esta es otra línea.\n')

# #Ejemplo 5: Modo de anexar (append) al final del archivo existente
# with open('archivo.txt', 'a') as archivo:
#     archivo.write('Añadiendo una nueva línea al final del archivo.\n')

# #With para manejar excepciones
# class MiContextManager:
#     def __enter__(self):
#         print("Entrando al contexto")
#         return self  # Puede devolver un objeto

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("Saliendo del contexto")
#         if exc_type:
#             print(f"Ocurrió una excepción: {exc_val}")

# # Uso del context manager
# with MiContextManager() as manager:
#     print("Dentro del contexto")
#     # Puedes lanzar una excepción aquí para ver cómo se maneja
#     raise ValueError("Un error ocurrió")

#--------------------------------------------------------------------------------------------------
#Decorators + context manager

#Decorador @contextlib.contextmanager junto con un generador para crear un administrador de contexto llamado timer.
# Este administrador de contexto mide el tiempo que tarda en ejecutarse el bloque de código dentro de with timer()
@contextlib.contextmanager
def timer():
  start = time.time()
  # Send control back to the context block
  try:
    yield   # (acá es donde se corre lo que se pone luego de la llamada del with.)
  finally:
    end = time.time()
    print('Elapsed: {:.2f}s'.format(end - start))

# with timer():
#   print('This should take approximately 0.25 seconds')
#   time.sleep(0.25)

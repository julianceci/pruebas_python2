import sys, time, textwrap, contextlib, inspect
import numpy as np
import pandas as pd
 
#sys.exit()
##########################################################################################################

#--------------------------------------------------------------------------------------------------
#Ejercicio de cajas de Despe
def difcajas(cajas: list[int]) -> list[(int, int)]:
  """
    Calcula ajustes que hay que aplicar para que la matriz quede pareja.

    Args:
        cajas (float): array con cantidad de cajas en cada columna.
        width (float): The width of the rectangle.

    Returns:
        float: array que retorna los austes que hay que hacer en cada columna.
    
    Raises:
        N/A.

    Example:
      >>> difcajas([6,2,5,6,1,4])
      [(1, -2), (2, 2), (3, -1), (4, -2), (5, 3), (6, 0)]
  """  
    
  cajas = [6,2,5,6,1,4]
  tamcol = int(sum(cajas)/len(cajas))
    
  return [(i+1, tamcol-cajas[i]) for i in range(0, len(cajas))]

cajas = [6,2,5,6,1,4]

print(cajas)
print(difcajas(cajas))
print(inspect.getdoc(difcajas))

#--------------------------------------------------------------------------------------------------
# Cosas de NP arrays ------------------------------------------------------------------------------

def np_work():

  x = np.array([[1, 2], [3, 4]])
  y = np.array([[5, 6], [7, 6]])
  #print(np.vstack((x, y)))
  #print(np.concatenate((x, y), axis=0))
  #print(np.concatenate((x, y), axis=1).reshape(4,2))

  x = np.array([1, 2, 3, 4])
  x2 = x[:, np.newaxis]
  #print(x2.shape)
  #print(x2)
  
  x2 = x.reshape(4, 1)
  #print(x2.shape)
  #print(x2)

  a1d = np.arange(1, 8, 2) #start, stop, step!
  a2d = np.array([[1, 2, 3],[1, 3, 4]])
  aEmp = np.empty((4,2)) #shape de array con valores random
  aOnes = np.ones((4,2)) #shape de array con 1
  aRnd = np.random.randint(low=0, high=100, size=4) #array con valores int aleatorios
  # print(a1d)
  # print(a1d.shape)
  # print(a2d)
  # print(a2d[0:,1:3])
  # print(aEmp)
  # print(aOnes)
  # print(aRnd)

  nparr = np.random.randint(low=0, high=100, size=10) #array con valores int aleatorios
  # print(nparr)

  # nparr.sort()
  # print(nparr)
  # print(nparr.sum())

  # print(nparr[2:4])
  # print(nparr[nparr<60])
  # print(nparr*2)

np_work()

#--------------------------------------------------------------------------------------------------
def contieneString(text1, text2):
  """ 
  recorre el text1 y devuelve true si el text2 esta contenido en el.

  :param text1: texto evaluar si contiene text2
  :param text2: texto a evaluar si está contenido en text2
  :return: true o false
  >>> contieneString('the rain in spain', 'in spain')
  True
 """
  
  contieneSTR = False
  contieneSTR = text1.find(text2) != -1
  
  #for i in range(0, len(text1)):
  #  contieneSTR = contieneSTR or text1.startswith(text2, i)

  #for i in range(0, len(text1)):
  #  if i+len(text2) < len(text1): contieneSTR = contieneSTR or (text1[i:i+len(text2)] == text2)
  
  #for i in range(0, len(text1)):
  #  coincidenSTRs = True
  #  for j in range(0, len(text2)):
  #    coincidenSTRs = coincidenSTRs and (text1[i+j] == text2[j])
  #  contieneSTR = contieneSTR or coincidenSTRs
  
  return contieneSTR

str1 = 'aHola como te v fsdfsdf te vad lskdg'
str2 = 'te va'

#print(contieneString(str1, str2))

#--------------------------------------------------------------------------------------------------
# Ejercicios de Mutantes de Meli ------------------------------------------------------------------
def isMutant(dna):
  dnaBase = ["AAAA", "TTTT", "CCCC", "GGGG"]
  
  #Horizontal cases
  posibleValues = dna

  #Vertical cases
  vertical = []
  for i in range(len(dna)):
    vertical.append(''.join(list(x[i] for x in dna)))

  posibleValues = posibleValues + vertical

  #diagonal cases
  diagonal = []
  for i in range(len(dna)):
    diagonalIt1 = ""
    diagonalIt2 = ""
    diagonalIt3 = ""
    diagonalIt4 = ""
    for j in range(i, len(dna)):
      diagonalIt1 = diagonalIt1 + dna[j-i][j]
      diagonalIt2 = diagonalIt2 + dna[len(dna)-1-(j-i)][j]
      diagonalIt3 = diagonalIt3 + dna[j][j-i]
      diagonalIt4 = diagonalIt4 + dna[len(dna)-1-(j)][j-i]
    diagonal = diagonal + [diagonalIt1] + [diagonalIt2] + [diagonalIt3] + [diagonalIt4]

#  print(diagonal)
  posibleValues = posibleValues + diagonal
  
  #saco duplicados!
  posibleValues = list(set(posibleValues))

#  print(posibleValues)

  result = list(x for x in posibleValues for y in dnaBase if not x.find(y))
  print(result)

  return len(result) > 0


dnaNP = [
"ATGCGA",
"CAGTGC",
"TTATGT",
"AGAATG",
"CCCTTA",
"TCTCTG"
]


dnaNP = [
"ATGCGA",
"CAGTGC",
"TTATGT",
"AGAAGG",
"CCCCTA",
"TCACTG"
]

#print(isMutant(dnaNP))

#--------------------------------------------------------------------------------------------------
#Ejercicio Meli: encontrar los pares de con mínima distancia ------------------

def minDistPairs(input):

  input.sort()
  print(input)

  difMinima = input[1]-input[0]
  listaResult = [[input[1], input[0]]]

  for i in range(1, len(input)-1):
    difTmp = input[i+1]-input[i]
    if difTmp == difMinima:
      listaResult.append([input[i+1], input[i]])
    elif difTmp < difMinima:
      difMinima = difTmp
      listaResult = [[input[i+1], input[i]]]
  
  return (difMinima, listaResult)

input = [8, 30, 2, 20, 10, 5, 15, 21, 31]

#print(minDistPairs(input))

#--------------------------------------------------------------------------------------------------
# Varios ------------------------------------------------------------------------------

def varios():
  #Jugando con listas --------------------------------------------------------------
  #Parseos --------
  string = "ABCDEFGHIJKLIMNOQRSTUVWXYZ"
  word_list = textwrap.wrap(text=string, width=4)
  print(word_list)
  #para ver los elemntos de la lista x renglón
  print("\n".join(word_list)) #OpciónA joineando
  print(*word_list, sep="\n") #OpciónB desempacando

  #tuplas, usando set para sacar repetidos --------
  listSN = [["Jarry", 40.21], ["Barry", 33.1], ["Terry", 37.21], ["Mary", 37.21]]
  scores = [t[1] for t in listSN]

  print(f"lista de pares name, score: {listSN}")
  print(f"lista de score: {scores}")

  minscoreUNQ = list(set(scores))
  print(f"lista sin repetidos pasando a set: {minscoreUNQ}")

  minscoreUNQ.remove(min(minscoreUNQ))
  secondScore = min(minscoreUNQ)

  namesresult = []
  for item in listSN:
      if item[1] == secondScore:
          namesresult.append(item[0])
  print(f"lista de names con el 2do menor score: {namesresult}")

  #creo lista de enterios en base a un string
  intlist = list(map(int, "2 3 6 6 5".split()))

  #Jugando con diccionarios ------------------------------------------------------------
  student_marks = {}
  student_marks["Carlos"] = [20, 30, 70]
  student_marks["Pedro"] = [20, 30, 100]
  print (student_marks)

  number = sum(student_marks["Carlos"])/len(student_marks["Carlos"])
  print(f'Promedio de marks de Carlos: {number:1.2f}')

  #uso doble de list comprenhension
  str1='hola'
  str2='1234'
  print([x + y for y in str1 for x in str2])

#varios()

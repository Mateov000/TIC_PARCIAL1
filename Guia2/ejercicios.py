import random
from utils import helpers

def deducir_fuente_memoria_nula(mensaje): #recibe cadena de caracteres emitidos por la fuente
    alfabeto = []                         # y devuelve listas paralelas (alfabeto, probabilidades)
    probabilidades = []
    alfabeto = []
    tamanio = len(mensaje)
    encuentros = []

    for letra in mensaje:
        if letra in alfabeto:
            indice = alfabeto.index(letra)
            encuentros[indice] += 1
        else:
            alfabeto.append(letra)
            encuentros.append(1)
            
    for encuentro in encuentros:
        probabilidades.append(encuentro/tamanio)
        
    return (alfabeto, encuentros)

def simular_palabra_fuente_memoria_nula(alfabeto, probabilidades, largo): #recibe lista de alfabeto, probabilidades y el largo deseado de la palabra
    return random.choices(alfabeto, probabilidades, k=largo)              #devuelve lista con caracteres

def calcular_entropia_fuente_binaria(w):
    return helpers.entropia_desde_fuente([w, 1-w])

def normalizar_vector(vector):
    suma = sum(vector)
    return [p/suma for p in vector]

def deducir_fuente_de_markov(mensaje):  # devuelve alfabeto y matriz_transicion
                                        # el ultimo simbolo no puede aparecer una sola vez 
                                        # porque no determina probabilidades en la matriz de transicion
    alfabeto = []
    for simbolo in mensaje:
        if simbolo not in alfabeto:
            alfabeto.append(simbolo)

    N = len(alfabeto)
    matriz_transicion = [[0] * N for fila in range(N)]
    for i_mensaje in range(len(mensaje) - 1):
        col = alfabeto.index(mensaje[i_mensaje])      #j
        fila = alfabeto.index(mensaje[i_mensaje + 1])  #i
        matriz_transicion[fila][col] += 1
        
    for col in range(N):
        columna_normal = normalizar_vector([fila[col] for fila in matriz_transicion]) #vector que es la columna con las probabilidades
        for fila in range(N):
            matriz_transicion[fila][col] = columna_normal[fila]
            
    return alfabeto, matriz_transicion

def simular_palabra_fuente_de_markov(alfabeto, matriz_transicion, largo):
    palabra = []
    
    #elijo primer simbolo dependiendo del vector estacionario
    v_estacionario = helpers.generar_vector_estacionario(matriz_transicion)
    palabra.append(random.choices(alfabeto, v_estacionario)[0])
    
    for i_char in range(largo-1):
        indice = alfabeto.index(palabra[i_char])
        probabilidades = helpers.getColumna(matriz_transicion,indice)
        palabra.append(random.choices(alfabeto, probabilidades)[0])
        
    return "".join(palabra)

def deducir_si_memoria_nula_o_markoviana(matriz_transicion, tolerancia): #true si es memoria nula, false de lo contrario (markoviana o con memoria)
    maxdif = 0
    N = len(matriz_transicion)
    for j in range(N):
        if (max(matriz_transicion[j]) - min(matriz_transicion[j])) > tolerancia: #diferencia maxima en una misma fila deberia ser menor a la tolerancia
            return False
    return True
            
    
def ejercicio_16(cadena, tolerancia):
    alfabeto, matriz = deducir_fuente_de_markov(cadena)
    if(deducir_si_memoria_nula_o_markoviana(matriz, tolerancia)):
        print("Es de memoria nula")
    else:
        print("Es con memoria")
    print("Su entropia es " + str(helpers.entropia_desde_fuente_markov(matriz)))
    

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--ejecutar", "-e", action="store_true")
args = parser.parse_args()
if(args.ejecutar): 
    tolerancia = 0.1   
    ejercicio_16("CAAACCAABAACBBCABACCAAABCBBACC", tolerancia)
    ejercicio_16("BBAAACCAAABCCCAACCCBBACCAABBAA", tolerancia)
    
    
    

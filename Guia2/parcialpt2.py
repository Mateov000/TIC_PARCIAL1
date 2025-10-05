import math
def getColumna(matriz, i):
    return [fila[i] for fila in matriz]
def get_simbolos_unicos(palabras_codigo): #devuelve una cadena con los simbolos
    cadena = ""
    for palabra in palabras_codigo:
        for simbolo in palabra:
            if simbolo not in cadena:
                cadena += simbolo
    return cadena

def es_no_singular(codigo):
    return len(set(codigo)) == len(codigo)
def es_instantaneo(codigo):
    codigo = sorted(codigo)
    for a, b in zip(codigo, codigo[1:]): #basta comparar uno con el siguiente porque estan en orden, entonces x es prefijo de y, al ordenarlos no puede haber un z entre ellos del que x no sea prefijo
        if b[:len(a)] == a: #b empieza con a, a es prefijo de b
            return False
    return True

from itertools import product
def es_univocamente_decodificable(codigo):
    if not es_no_singular(codigo):
        return False
    if "" in codigo:
        return False
    
    def determinar_terminar(S):
        for palabra in S[-1]: #alguna palabra del ultimo codigo de Si esta en S1
            if palabra in S[0]:
                return True, False #no es UD
        for codigo in S[:-1]: #algun codigo de Si es igual a otro de Si
            if codigo == S[-1]: #solo chequea si el ultimoa agregado es igual a alguno de los anteriores (excluyendo el ultimo)
                return True, True #el codigo es UD
        return False, None
    
    esUD = False
    S = [set(codigo)] #lista de sets
    
    while True:
        Snuevo = set()
        for x, y in list(product(S[0], S[-1])):
            sufijo = y.removeprefix(x)
            if sufijo == "":
                if len(S) > 1: #innecesario porque ya lo habria detectado determinar_terminar
                    return False
            else:
                if sufijo != y:
                    Snuevo.add(sufijo)
                sufijo = x.removeprefix(y)
                if sufijo != x:
                    Snuevo.add(sufijo)
        S.append(Snuevo)
        termino, esUD = determinar_terminar(S)
        if termino:
            break
    return esUD
        
        
def es_compacto(codigo, probabilidades):
    r = len(get_simbolos_unicos(codigo))
    if es_instantaneo(codigo):
        for palabra, probabilidad in zip(codigo, probabilidades):
            if len(palabra) > math.ceil(math.log(1/probabilidad, r)):
                return False
        return True
    return False
    
def generar_lista_longitudes_de_palabras(palabras_codigo):
    return [len(palabra) for palabra in palabras_codigo]

def sumatoria_Kraft(palabras_codigo):
    r = len(get_simbolos_unicos(palabras_codigo))
    suma = 0
    for li in generar_lista_longitudes_de_palabras(palabras_codigo):
        suma += r**(-li)
    return suma
    
def calcular_longitud_media(palabras_codigo, probabilidades):
    return sum(longitud*probabilidad for longitud, probabilidad in zip(generar_lista_longitudes_de_palabras(palabras_codigo), probabilidades))

codigo = ["])", "(", ")[", "[", "(]"]
probabilidades= [0.15, 0.25, 0.05, 0.45, 0.10]
print(calcular_longitud_media(codigo, probabilidades))
def entropia_memoria_nula(probabilidades): #recibe lista de probabilidades
    entropia = 0
    for probabilidad in probabilidades:
        if probabilidad != 0:
            entropia += probabilidad * math.log2(1/probabilidad)
    return entropia

print(entropia_memoria_nula(probabilidades))

print(es_instantaneo(codigo))
print(es_no_singular(codigo))
print(es_univocamente_decodificable(codigo))
print(es_compacto(codigo, probabilidades))
print(sumatoria_Kraft(codigo))
print(entropia_memoria_nula(probabilidades))


codigo = [",;", ";", ":.", ".", ",:"]
probabilidades= [0.15, 0.25, 0.05, 0.45, 0.10]
print(calcular_longitud_media(codigo, probabilidades))
print(es_instantaneo(codigo))
print(es_no_singular(codigo))
print(es_univocamente_decodificable(codigo))
print(es_compacto(codigo, probabilidades))
print(sumatoria_Kraft(codigo))
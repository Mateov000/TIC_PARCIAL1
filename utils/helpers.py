#importo librerias nativas de python
import math

#defino las funciones


def lista_info_desde_lista_probabilidades(probabilidades): #desde lista de probabilidades
    return [calcular_info_evento(probabilidad) for probabilidad in probabilidades]


def generar_extension_memoria_nula(alfabeto, probabilidades, N): #devuelve (alfabeto,probabilidades) de extension orden N
    
    def extender(alf_fuente, prob_fuente, alf_act, prob_act):
        alf_extendido = []
        prob_extendido = []
        for i in range(len(alf_fuente)):
            for j in range(len(alf_act)):
                alf_extendido.append(alf_fuente[i] + alf_act[j])
                prob_extendido.append(prob_fuente[i] * prob_act[j])

        return alf_extendido, prob_extendido
    
    alfabeto_extendido = alfabeto                                      #si N es menor a 1 devuelve listas vacias
    probabilidades_extendidas = probabilidades
    
    for i in range(N):
        alfabeto_extendido, probabilidades_extendidas = extender(alfabeto, probabilidades, alfabeto_extendido, probabilidades_extendidas)
    return alfabeto_extendido, probabilidades_extendidas

def multiplicar_vectores(v1, v2):
    if(len(v1) != len(v2)):
        raise ValueError
    res = 0
    for i in range(len(v1)):
        res += v1[i]*v2[i]
    return res

def multiplicar_matriz_con_vector(matriz, vector):
    if (len(matriz[0]) != len(vector)):
        raise ValueError
    
    N = len(matriz)
    v_res = []
    for i in range(N):
        v_res.append(multiplicar_vectores(matriz[i], vector))
    return v_res

def generar_vector_estacionario(matriz_transicion): #matriz_transicion es una lista de listas donde matriz_transicion[i][j] 
                                                    #respresenta probabilidad de pasar de estado j a estado i
    tolerancia = 0.000001
    def generar_vector_equiprobable(N):
        return [1/N for p in range(N)]
    
    def diferencia_maxima_entre_vectores(v1, v2):
        maxdif = 0
        for i in range(len(v1)):
            dif = abs(v1[i]-v2[i])
            if dif > maxdif:
                maxdif = dif
        return maxdif
    
    N = len(matriz_transicion)
    v_ant = generar_vector_equiprobable(N)
    v_act = multiplicar_matriz_con_vector(matriz_transicion, v_ant)
    while(diferencia_maxima_entre_vectores(v_ant, v_act) > tolerancia):
        v_ant = v_act
        v_act = multiplicar_matriz_con_vector(matriz_transicion, v_ant)
    return v_act

def entropia_desde_fuente_markov(matriz_transicion): #recibe matriz transicion orden 1 #j es fila e i es columna 
    v_estacionario = generar_vector_estacionario(matriz_transicion)
    entropia = 0
    N = len(v_estacionario)
    for i in range(N):
        v_posibilidades = [fila[i] for fila in matriz_transicion] #distribucion de probabilidades de siguiente simbolo dado un simbolo i, es la columna i de la matriz
        entropia += v_estacionario[i] * entropia_desde_fuente(v_posibilidades)
    return entropia
        
def getColumna(matriz, i):
    return [fila[i] for fila in matriz]


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
        
    

#teoremas

def calcular_info_evento(probabilidad): #devuelve informacion relacionada a un evento de probabilidad "probabilidad"
    if probabilidad == 0: return math.inf
    return math.log2(1/probabilidad)

def calcular_info_evento_base_r(probabilidad, r): #devuelve informacion relacionada a un evento de probabilidad "probabilidad"
    if probabilidad == 0: return math.inf
    return math.log(1/probabilidad, r)

def entropia_desde_fuente(probabilidades): #recibe lista de probabilidades
    infos = lista_info_desde_lista_probabilidades(probabilidades)
    entropia = sum(p*i for p, i in zip(probabilidades, infos))
    return entropia

def entropia_base_r_desde_fuente(probabilidades, r):
    return sum(p*calcular_info_evento_base_r(p, r) for p in probabilidades)
    
def es_compacto(codigo, probabilidades):
    r = len(get_simbolos_unicos(codigo))
    if es_instantaneo(codigo):
        for palabra, probabilidad in zip(codigo, probabilidades):
            if len(palabra) > math.ceil(math.log(1/probabilidad, r)):
                return False
        return True
    return False

def entropia_extension(probabilidades_fuente, N_extension):
    return entropia_desde_fuente(probabilidades_fuente) * N_extension



#guia 3, ejercicio 9
def get_simbolos_unicos(palabras_codigo): #devuelve una cadena con los simbolos
    cadena = ""
    for palabra in palabras_codigo:
        for simbolo in palabra:
            if simbolo not in cadena:
                cadena += simbolo
    return cadena
"""def get_simbolos_unicos(palabras):
    return ''.join(dict.fromkeys(''.join(palabras)))"""
    
def generar_lista_longitudes_de_palabras(palabras_codigo):
    return [len(palabra) for palabra in palabras_codigo]

def sumatoria_Kraft(palabras_codigo):
    r = len(get_simbolos_unicos(palabras_codigo))
    suma = 0
    for li in generar_lista_longitudes_de_palabras(palabras_codigo):
        suma += r**(-li)
    return suma

#ejercicio 11

def calcular_longitud_media(palabras_codigo, probabilidades):
    return sum(longitud*probabilidad for longitud, probabilidad in zip(generar_lista_longitudes_de_palabras(palabras_codigo), probabilidades))

#utiles para chequear


def es_ergodica_por_columnas(P, eps=1e-12, max_t=None):
    # Suficiente (rápido): si todas las entradas son > 0, es ergódica
    N = len(P)
    todas_positivas = True
    for i in range(N):
        for j in range(N):
            if P[i][j] <= eps:
                todas_positivas = False
                break
        if not todas_positivas:
            break
    if todas_positivas:
        return True

    # Irreducibilidad: grafo fuertemente conexo (arista j->i si P[i][j] > eps)
    adj = [[] for _ in range(N)]
    for j in range(N):
        for i in range(N):
            if P[i][j] > eps:
                adj[j].append(i)

    def dfs(start, grafo):
        visto = [False]*N
        pila = [start]
        visto[start] = True
        while pila:
            u = pila.pop()
            for v in grafo[u]:
                if not visto[v]:
                    visto[v] = True
                    pila.append(v)
        return visto

    visto1 = dfs(0, adj)
    if not all(visto1):
        return False

    # Grafo reverso
    radj = [[] for _ in range(N)]
    for u in range(N):
        for v in adj[u]:
            radj[v].append(u)
    visto2 = dfs(0, radj)
    if not all(visto2):
        return False

    # Aperiodicidad: si hay auto-bucle en algún estado, basta
    for i in range(N):
        if P[i][i] > eps:
            return True

    # Si no hay auto-bucles, chequeo del período vía potencias
    # (suficientemente bueno en práctica)
    if max_t is None:
        max_t = 4 * N * N

    def multiplicar(A, B):
        C = [[0.0]*N for _ in range(N)]
        for i in range(N):
            for k in range(N):
                aik = A[i][k]
                if aik <= eps:
                    continue
                for j in range(N):
                    C[i][j] += aik * B[k][j]
        return C

    M = [fila[:] for fila in P]  # P^1
    g = 0
    estado = 0  # en irreducibles el período es igual para todos
    for t in range(1, max_t+1):
        if M[estado][estado] > eps:
            g = math.gcd(g, t) if g else t
            if g == 1:
                return True
        M = multiplicar(M, P)

    return g == 1
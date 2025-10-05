import math

def deducirAlfabetoYProbabilidades(mensaje):
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
        
    return (alfabeto, probabilidades)

def normalizar_vector(vector):
    suma = sum(vector)
    return [p/suma for p in vector]

def generarMatrizTransicion(mensaje, alfabeto):
    
    N = len(alfabeto)
    matriz_transicion = [[0] * N for fila in range(N)] #la inicializo en 0
    
    for i_mensaje in range(len(mensaje) - 1):
        col = alfabeto.index(mensaje[i_mensaje])      #j
        fila = alfabeto.index(mensaje[i_mensaje + 1])  #i
        matriz_transicion[fila][col] += 1
        
    for col in range(N):
        columna_normal = normalizar_vector([fila[col] for fila in matriz_transicion]) #vector que es la columna con las probabilidades
        
        for fila in range(N):
            matriz_transicion[fila][col] = columna_normal[fila]
            
    return matriz_transicion
    

def deducir_si_memoria_nula_o_no_nula(matriz_transicion, tolerancia): #true si es memoria nula, false de lo contrario (markoviana o con memoria)
    N = len(matriz_transicion)
    for j in range(N):
        if (max(matriz_transicion[j]) - min(matriz_transicion[j])) > tolerancia: #diferencia maxima en una misma fila deberia ser menor a la tolerancia
            return False
    return True

def entropia_memoria_nula(probabilidades): #recibe lista de probabilidades
    entropia = 0
    for probabilidad in probabilidades:
        if probabilidad != 0:
            entropia += probabilidad * math.log2(1/probabilidad)
    return entropia

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
    
    for i in range(N-1):
        alfabeto_extendido, probabilidades_extendidas = extender(alfabeto, probabilidades, alfabeto_extendido, probabilidades_extendidas)
    return alfabeto_extendido, probabilidades_extendidas

def entropia_extension(probabilidades_fuente, N_extension):
    return entropia_memoria_nula(probabilidades_fuente) * N_extension

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

def entropia_desde_fuente_markov(matriz_transicion, v_estacionario): #recibe matriz transicion orden 1 #j es fila e i es columna 
    entropia = 0
    N = len(v_estacionario)
    for i in range(N):
        v_posibilidades = [fila[i] for fila in matriz_transicion] #distribucion de probabilidades de siguiente simbolo dado un simbolo i, es la columna i de la matriz
        entropia += v_estacionario[i] * entropia_memoria_nula(v_posibilidades)
    return entropia


def ejercicioParcial(mensaje):
    alfabeto, probabilidades = deducirAlfabetoYProbabilidades(mensaje)
    """ alfabeto = ["*", "+","-","/"]
    alfabeto = [",", ".",":",";"] """    #uso esto para ordenar la matriz como esta en el parcial, solo con fines esteticos
    matriz_transicion = generarMatrizTransicion(mensaje, alfabeto)
    tolerancia = 0.1
    esMemoriaNula = deducir_si_memoria_nula_o_no_nula(matriz_transicion, tolerancia)

    print("Alfabeto: ", alfabeto)
    print("Probabilidades: ", probabilidades)
    print("Matriz de transicion por columnas: ", matriz_transicion)
    
    if(esMemoriaNula):
        alfabeto_extendido, probabilidades_extendidas = generar_extension_memoria_nula(alfabeto, probabilidades, 2)
        entropia_fuente_extendida = entropia_extension(probabilidades, 2)
        entropia = entropia_memoria_nula(probabilidades)
        print("Es una fuente de memoria nula")
        print("Su entropia es: ", entropia)
        for i in range(len(alfabeto_extendido)):
            print("Par simbolo/probabilidad: ", alfabeto_extendido[i], probabilidades_extendidas[i])
        print("La entropia de su extension de orden 2 es: ", entropia_fuente_extendida)
    else:
        vec_estacionario = generar_vector_estacionario(matriz_transicion)
        entropia = entropia_desde_fuente_markov(matriz_transicion, vec_estacionario)
        print("Es una fuente de memoria no nula")
        print("Su entropia es: ", entropia)
        print("Su vector estacionario es: ", vec_estacionario)
        
ejercicioParcial(";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;")
ejercicioParcial("-+-+*//++///*/-////+---////-+/+--+-+/-/+-+/-+*++//")
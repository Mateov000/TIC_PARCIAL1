from utils import helpers

def ejercicio_11(codigo, probabilidades):
    print("entropia: " + str(helpers.entropia_desde_fuente(probabilidades)))
    print("longitud media: " + str(helpers.calcular_longitud_media(codigo, probabilidades)))
    
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--ejecutar", "-e", action="store_true")
args = parser.parse_args()
if(args.ejecutar): 
    ejercicio_11(["0","10","01","11"], [0.2,0.3,0.22,0.28])
    print("Es compacto" if helpers.es_compacto([".,", ";",",,",":","...",",:;"], [0.1,0.5,0.1,0.2,0.05,0.05]) else "No es compacto")
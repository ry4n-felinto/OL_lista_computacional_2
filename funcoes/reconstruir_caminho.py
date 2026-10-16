import numpy as np

def reconstruir_caminho(anterior, s, t):

    caminho_inverso = [] 

    i = t

    while i != s:
        if i == -1:
            return []
        
        caminho_inverso.append(i)
        i = anterior[i]

    caminho_inverso.append(s)

    return caminho_inverso[::-1]

def calcular_metricas(caminho, s, t):

    if caminho:

        custo = len(caminho)
        arestas = len(caminho)
        vertices = len(caminho)+1

        return custo, arestas, vertices

    else:

        return np.inf, 0, 0
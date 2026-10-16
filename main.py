import matplotlib.pyplot as plt
import numpy as np
from funcoes.encontrar_extremos import encontrar_extremos
from PIL import Image

from funcoes.construir_grafo import construir_grafo
from funcoes.id_no import id_no
from funcoes.dijkstra import dijkstra
from funcoes.reconstruir_caminho import reconstruir_caminho
from funcoes.reconstruir_caminho import calcular_metricas
from funcoes.visualizacao import visualizar_caminho
from funcoes.visualizacao import visualizar_grafo_caminho

# Ler a imagem para processamento
img = np.array(Image.open("labirinto.jpeg"))

# Converte a imagem para escalas de cinza
if img.ndim == 3:
    img = np.array(Image.open("labirinto.jpeg").convert("L"))

# Plota a imagem original
plt.figure()
plt.imshow(img, cmap = "gray")
plt.title("Imagem original do labirinto")
plt.axis("off")
plt.show()

# Localiza os pixels escuros para delimitar o labirinto
linhas_escuras, colunas_escuras = np.where(img < 128)

linha_min = linhas_escuras.min()
linha_max = linhas_escuras.max()
coluna_min = colunas_escuras.min()
coluna_max = colunas_escuras.max()

# Recorta a margem branca externa
img_nova = img[
    linha_min:linha_max + 1,
    coluna_min:coluna_max + 1
]

# Transforma a imagem em uma matriz binaria
""" A matriz considera o numero de pixels da imagem. 
    A matriz e formada por 41x41 celulas e 20x20 arestas.
    0 = parede, 1 = caminho livre
"""
matriz_binaria = (img_nova > 128).astype(int)
print(matriz_binaria)
print("Formato da matriz:", matriz_binaria.shape)


# Transforma a matriz binaria em uma imagem binaria
plt.figure()
plt.imshow(matriz_binaria, cmap = "gray")
plt.title("Imagem binaria do labirinto")
plt.axis("off")
plt.show()

# Armazena as coordenadas do vertice da entrada e da saida
x, pixels = encontrar_extremos(matriz_binaria)
print("Entrada e saída:", x)
print("Pixels das aberturas:", pixels)

from funcoes.construir_grafo import coordenadas_centros

m = n = 20

A = construir_grafo(matriz_binaria, m, n)

print("Formato da matriz de adjacência:", A.shape)
print("Número de arestas:", np.sum(A) // 2)

s = id_no(x[0][0], x[0][1], n)
t = id_no(x[1][0], x[1][1], n)

print(s, t)

# Noto que são os IDs começando em 1. Como o Dijkstra do Lucas e a matriz A
# usam índices começando em 0, na chamada do Dijkstra usamos s - 1. Para reconstruir o caminho,
# também usamos índices começando em 0.

dist, predecessores = dijkstra(A, s-1 )

print("Distância até a saída:", dist[t-1])
print("Predecessor da saída:", predecessores[t-1])

caminho = reconstruir_caminho(predecessores, s -1, t-1)

print("Caminho encontrado:", caminho)
print("Quantidade de vértices:", len(caminho))

custo, arestas, vertices = calcular_metricas(caminho, s-1, t-1)

print("Custo do caminho:", custo)
print("Número de arestas:", arestas)
print("Número de vértices:", vertices)

caminho_ids = [vertice + 1 for vertice in caminho]

visualizar_caminho(img_nova, caminho_ids, m, n, s, t, pixels)

print("Primeiro ID:", caminho_ids[0])
print("Último ID:", caminho_ids[-1])
print("Entrada e saída:", x)

# (b) Grafo sobre o labirinto
visualizar_grafo_caminho(
    matriz_binaria, A, m, n,
    mostrar_labirinto=True,
    nome_arquivo="grafo_sobre_labirinto.png"
)

# (d) Grafo completo com caminho mínimo
visualizar_grafo_caminho(
    matriz_binaria, A, m, n,
    caminho=caminho_ids,
    mostrar_labirinto=False,
    nome_arquivo="grafo_com_caminho.png"
)
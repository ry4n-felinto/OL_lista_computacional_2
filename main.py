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
x = encontrar_extremos(matriz_binaria)
print(" Entrada e saída:", x)

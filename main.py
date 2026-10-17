from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from funcoes.encontrar_extremos import encontrar_extremos
from funcoes.construir_grafo import construir_grafo
from funcoes.id_no import id_no
from funcoes.dijkstra import dijkstra
from funcoes.reconstruir_caminho import (reconstruir_caminho,calcular_metricas,
)
from funcoes.visualizacao import (visualizar_caminho, visualizar_grafo_caminho,
)


def main():
    # ==================================================
    # 1. Leitura e processamento da imagem
    # ==================================================
    imagem_original = np.array(
        Image.open("labirinto.jpeg").convert("L")
    )

    # Recorta as margens externas.
    linhas, colunas = np.where(imagem_original < 128)

    linha_min, linha_max = linhas.min(), linhas.max()
    coluna_min, coluna_max = colunas.min(), colunas.max()

    img = imagem_original[
        linha_min:linha_max + 1,
        coluna_min:coluna_max + 1
    ]

    # 1 = caminho livre; 0 = parede.
    B = (img > 128).astype(int)

    print("Dimensão da imagem binária:", B.shape)

    # (a) Imagem original.
    plt.figure()
    plt.imshow(imagem_original, cmap="gray")
    plt.title("Labirinto original")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("labirinto_original.png", dpi=200,bbox_inches="tight")
    plt.show()

    # (b) Imagem binária.
    plt.figure()
    plt.imshow(B, cmap="gray")
    plt.title("Imagem binária do labirinto")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("labirinto_binario.png", dpi=200, bbox_inches="tight")
    plt.show()

    # ==================================================
    # 2. Identificação da entrada e da saída
    # ==================================================
    extremos, pixels = encontrar_extremos(B)

    print("Entrada e saída:", extremos)
    print("Pixels das aberturas:", pixels)

    # ==================================================
    # 3. Construção do grafo
    # ==================================================
    m = n = 20
    A = construir_grafo(B, m, n)

    numero_vertices = m * n
    numero_arestas = int(np.sum(A) // 2)

    print("Número de vértices:", numero_vertices)
    print("Número de arestas:", numero_arestas)

    # Identificadores dos vértices inicial e final.
    s = id_no(extremos[0][0], extremos[0][1], n)
    t = id_no(extremos[1][0], extremos[1][1], n)

    print("Vértice inicial:", s)
    print("Vértice final:", t)

    # (b) Grafo construído sobre o labirinto.
    visualizar_grafo_caminho(
        B, A, m, n,
        mostrar_labirinto=True,
        nome_arquivo="grafo_sobre_labirinto.png"
    )

    # ==================================================
    # 4. Dijkstra e reconstrução do caminho mínimo
    # ==================================================
    inicio = perf_counter()
    dist, predecessores = dijkstra(A, s - 1)
    tempo_execucao = perf_counter() - inicio

    caminho = reconstruir_caminho(
        predecessores, s - 1, t - 1
    )

    if caminho is None or len(caminho) == 0:
        raise ValueError("Não foi encontrado um caminho entre a entrada e a saída.")

    # Converte os IDs de 0-based para 1-based.
    caminho_ids = [int(v) + 1 for v in caminho]

    print("Distância mínima até a saída:", dist[t - 1])
    print("Custo do caminho:", calcular_metricas(
        caminho, s - 1, t - 1
    )[0])
    print("Número de vértices no caminho:", len(caminho))
    print("Número de movimentos:", len(caminho) - 1)
    print(f"Tempo de Dijkstra: {tempo_execucao:.6f} segundos")

    # ==================================================
    # 5. Visualização do caminho mínimo
    # ==================================================

    # (c) Apenas o caminho mínimo sobre o labirinto.
    visualizar_caminho(
        img, caminho_ids, m, n, s, t, pixels
    )

    # (d) Grafo completo com o caminho mínimo destacado.
    visualizar_grafo_caminho(
        B, A, m, n,
        caminho=caminho_ids,
        mostrar_labirinto=False,
        nome_arquivo="grafo_com_caminho.png"
    )


if __name__ == "__main__":
    main()

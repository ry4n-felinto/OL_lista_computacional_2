import numpy as np 
import matplotlib.pyplot as plt

from funcoes.coordenada_no import coordenada_no
from funcoes.id_no import id_no
from funcoes.construir_grafo import coordenadas_centros


def visualizar_caminho(img, caminho, m, n, s, t, pixels):
    """Desenha o caminho mínimo sobre a imagem do labirinto.

    Parâmetros:
        img: imagem original do labirinto.
        caminho: lista ordenada de IDs dos vértices do caminho.
        m: número de linhas da grade.
        n: número de colunas da grade.
        s: ID do vértice de origem.
        t: ID do vértice de destino.
    """

    altura, largura = img.shape[:2]

    # converte cada ID em coordenadas de pixels.
    pontos = []

    for vertice in caminho:
        linha = (vertice - 1) // n + 1
        coluna = (vertice - 1) % n + 1

        x, y = coordenada_no(
            linha, coluna, largura, altura, n, m
        )
        pontos.append((x, y))

    # separa as coordenadas horizontais e verticais
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]

    # cria a figura
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img, cmap="gray", origin="upper")

    # desenha o caminho mínimo em vermelho
    ax.plot(xs, ys, color="red", linewidth=2.5, zorder=3, label="Caminho mínimo")
    # pixels contém [linha, coluna] detectados pela Julia
    linha_entrada, coluna_entrada = pixels[0]
    linha_saida, coluna_saida = pixels[1]

    # marca a entrada em verde
    ax.scatter(
        coluna_entrada, linha_entrada,
        color="green", s=80,
        label="Entrada", zorder=4
    )

    # marca a saída em azul
    ax.scatter(
        coluna_saida, linha_saida,
        color="blue", s=80,
        label="Saída", zorder=4
    )

    ax.set_title("Caminho mínimo no labirinto")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    ax.set_axis_off()
    fig.tight_layout()

    fig.savefig("caminho.png", dpi=200, bbox_inches="tight")
    plt.show() 

def visualizar_grafo_caminho(
    B, A, m, n,
    caminho=None,
    mostrar_labirinto=True,
    nome_arquivo="grafo.png"
    ):

        """
        Desenha os vértices e as arestas sobre o labirinto,
        sem desenhar a grade.
        """
        if B.ndim != 2:
            raise ValueError("A imagem binária deve ser bidimensional.")

        if A.shape != (m * n, m * n):
            raise ValueError("A dimensão da matriz A é incompatível.")

        altura, largura = B.shape
        xs, ys = coordenadas_centros(B, m, n)

        fig, ax = plt.subplots(figsize=(14, 12))

        if mostrar_labirinto:
            ax.imshow(
            B,
            cmap="gray",
            origin="upper",
            interpolation="nearest"
            )

        # Desenha somente as arestas existentes.
        for i in range(m):
            for j in range(n):
                u = i * n + j

                # Aresta para a direita.
                if j + 1 < n and A[u, u + 1] == 1:
                    ax.plot(
                        [xs[j], xs[j + 1]],
                        [ys[i], ys[i]],
                        color="red",
                        linewidth=1.2,
                        zorder=2
                    )

                # Aresta para baixo.
                if i + 1 < m and A[u, u + n] == 1:
                    ax.plot(
                        [xs[j], xs[j]],
                        [ys[i], ys[i + 1]],
                        color="red",
                        linewidth=1.2,
                        zorder=2
                    )

        # Desenha todos os vértices.
        for i in range(m):
            for j in range(n):
                ax.scatter(
                    xs[j],
                    ys[i],
                    color="blue",
                    s=12,
                    zorder=3
                )


        # Destaca o caminho mínimo.
        if caminho:
            pontos_x = []
            pontos_y = []

            for vertice in caminho:
                linha = (vertice - 1) // n
                coluna = (vertice - 1) % n

                pontos_x.append(xs[coluna])
                pontos_y.append(ys[linha])

            ax.plot(
                pontos_x, pontos_y,
                color="yellow",
                linewidth=2.5,
                zorder=4,
                label="Caminho mínimo"
            )

            ax.scatter(
                pontos_x[0], pontos_y[0],
                color="green", s=70,
                zorder=5, label="Início do caminho mínimo"
            )

            ax.scatter(
                pontos_x[-1], pontos_y[-1],
                color="blue", s=70,
                zorder=5, label="fim do caminho"
            )

            ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))

        titulo = (
            "Grafo completo com caminho mínimo"
            if caminho and not mostrar_labirinto
            else "Grafo sobreposto ao labirinto"
        )

        ax.set_title(titulo)
        ax.set_xlim(-0.5, largura - 0.5)
        ax.set_ylim(altura - 0.5, -0.5)
        ax.set_aspect("equal")
        ax.set_axis_off()

        plt.tight_layout()

        fig.savefig(nome_arquivo, dpi=200, bbox_inches="tight")
        plt.show()
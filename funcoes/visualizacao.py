import matplotlib.pyplot as plt

from funcoes.coordenada_no import coordenada_no
from funcoes.construir_grafo import coordenadas_centros


def visualizar_caminho(img, caminho, m, n, pixels):
    """Desenha o caminho mínimo sobre a imagem do labirinto.

    Parâmetros:
        img: imagem original do labirinto.
        caminho: lista ordenada de IDs dos vértices do caminho.
        m: número de linhas da grade.
        n: número de colunas da grade.
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

def visualizar_grafo_caminho(B, A, m, n, caminho=None,mostrar_labirinto=True,nome_arquivo="grafo.png"):

        """Visualiza o grafo construído a partir do labirinto.
           Ou destaca o caminho mínimo encontrado sobre o grafo.

        Parâmetros:
            B: imagem binária do labirinto.
            A: matriz de adjacência do grafo.
            m: número de linhas da grade.
            n: número de colunas da grade.
            caminho: lista ordenada de IDs dos vértices do caminho mínimo.
                    Se None ou vazia, o caminho não é destacado.
            mostrar_labirinto: se True, exibe a imagem do labirinto ao fundo;
                            se False, exibe somente o grafo.
            nome_arquivo: nome do arquivo em que a figura será salva.
        """
        if B.ndim != 2:
            raise ValueError("A imagem binária deve ser bidimensional.")

        if A.shape != (m * n, m * n):
            raise ValueError("A dimensão da matriz A é incompatível.")

        # altura = número de linhas de pixels; largura = número de colunas.
        altura, largura = B.shape

        # Calcula as coordenadas (x, y) dos centros das células da grade.
        # xs contém as posições horizontais das colunas.
        # ys contém as posições verticais das linhas.
        xs, ys = coordenadas_centros(B, m, n)

        # Cria uma figura e um eixo para desenhar o grafo.
        fig, ax = plt.subplots(figsize=(14, 12))


        # Verifica se a imagem do labirinto deve aparecer no fundo.
        if mostrar_labirinto:
                # Exibe a imagem binária em tons de cinza.
            ax.imshow(B, cmap="gray",origin="upper",interpolation="nearest")

        
        # Percorre todas as linhas da grade.
        for i in range(m):
            # Percorre todas as colunas da grade.
            for j in range(n):
                # Converte a posição (i, j), com índices começando em zero,
                # no índice correspondente do vértice na matriz de adjacência A.
                # A numeração dos vértices na matriz começa em zero.
                u = i * n + j

                # Verifica se existe uma coluna à direita
                # e se há uma aresta entre u e o vértice à direita.
                if j + 1 < n and A[u, u + 1] == 1:
                    # Desenha a aresta horizontal entre os centros das duas células.
                    ax.plot(
                        [xs[j], xs[j + 1]], # Coordenadas x: centro atual e centro à direita.
                        [ys[i], ys[i]],     # Coordenadas y: mesma linha.
                        color="red",
                        linewidth=1.2,
                        zorder=2
                    )
                # Verifica se existe uma linha abaixo
                # e se há uma aresta entre u e o vértice abaixo.
                if i + 1 < m and A[u, u + n] == 1:
                    ax.plot(
                        [xs[j], xs[j]],
                        [ys[i], ys[i + 1]],
                        color="red",
                        linewidth=1.2,
                        zorder=2
                    )

        # Percorre novamente todas as linhas da grade.
        for i in range(m):
            # Percorre todas as colunas da grade.
            for j in range(n):

                # Desenha o vértice localizado no centro da célula (i, j).
                ax.scatter(
                    xs[j],  # Coordenada horizontal do centro.
                    ys[i],  # Coordenada vertical do centro.
                    color="blue",
                    s=12,   # Tamanho do marcador.
                    zorder=3  # Desenha os vértices sobre as arestas.
                )


        # Destaca o caminho mínimo.
        if caminho:
            # Cria listas para armazenar as coordenadas dos vértices do caminho.
            pontos_x = []
            pontos_y = []

            # Percorre os IDs dos vértices na ordem do caminho.
            for vertice in caminho:
                # Converte o ID, que começa em 1, em índice de linha começando em zero.
                linha = (vertice - 1) // n

                # Converte o ID em índice de coluna começando em zero.
                coluna = (vertice - 1) % n

                # Guarda as coordenadas do centro desse vértice.
                pontos_x.append(xs[coluna])
                pontos_y.append(ys[linha])

            # Desenha o caminho conectando os vértices na ordem recebida.
            ax.plot(
                pontos_x, pontos_y,
                color="yellow",
                linewidth=2.5,
                zorder=4,     # O caminho aparece sobre os vértices e as arestas.
                label="Caminho mínimo"
            )
            # Destaca o primeiro vértice do caminho, o início.
            ax.scatter(
                pontos_x[0], pontos_y[0],
                color="green", s=70,
                zorder=5, label="Início do caminho mínimo"
            )

            # Destaca o último vértice do caminho, o destino.
            ax.scatter(
                pontos_x[-1], pontos_y[-1],
                color="blue", s=70,
                zorder=5, label="fim do caminho"
            )

            ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
            
        # Define o título conforme a presença do caminho e a exibição do labirinto.
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
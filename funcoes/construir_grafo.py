import matplotlib.pyplot as plt
import numpy as np


def coordenadas_centros(B: np.ndarray, m: int, n: int):
    """
    Calcula os centros das células da grade lógica.

    A imagem possui 2*m+1 subdivisões na altura e
    2*n+1 subdivisões na largura.
    """
    altura, largura = B.shape

    passo_y = altura / (2 * m + 1)
    passo_x = largura / (2 * n + 1)

    xs = [(2 * j + 1.5) * passo_x for j in range(n)]
    ys = [(2 * i + 1.5) * passo_y for i in range(m)]

    return xs, ys


def construir_grafo(B: np.ndarray, m: int, n: int) -> np.ndarray:
    """
    Constrói a matriz de adjacência.

    B: imagem binária, com 1 para caminho livre e 0 para parede.
    m: número de linhas de vértices.
    n: número de colunas de vértices.

    Retorna uma matriz de adjacência simétrica.
    """
    if B.ndim != 2:
        raise ValueError("A imagem binária deve ser bidimensional.")

    if m <= 0 or n <= 0:
        raise ValueError("m e n devem ser positivos.")

    altura, largura = B.shape

    if altura < 1 or largura < 1:
        raise ValueError("A imagem está vazia.")

    A = np.zeros((m * n, m * n), dtype=int)
    xs, ys = coordenadas_centros(B, m, n)

    def passagem_livre(x1, y1, x2, y2):
        x1, y1 = int(round(x1)), int(round(y1))
        x2, y2 = int(round(x2)), int(round(y2))

        # Verifica os limites da imagem.
        if not (
            0 <= x1 < largura
            and 0 <= x2 < largura
            and 0 <= y1 < altura
            and 0 <= y2 < altura
        ):
            return False

        # Movimento horizontal.
        if y1 == y2:
            pixels = B[
                y1,
                min(x1, x2):max(x1, x2) + 1
            ]

        # Movimento vertical.
        elif x1 == x2:
            pixels = B[
                min(y1, y2):max(y1, y2) + 1,
                x1
            ]

        else:
            return False

        return pixels.size > 0 and np.all(pixels == 1)

    for i in range(m):
        for j in range(n):
            u = i * n + j

            # Vizinho à direita.
            if j + 1 < n:
                v = u + 1

                if passagem_livre(
                    xs[j], ys[i],
                    xs[j + 1], ys[i]
                ):
                    A[u, v] = 1
                    A[v, u] = 1

            # Vizinho abaixo.
            if i + 1 < m:
                v = u + n

                if passagem_livre(
                    xs[j], ys[i],
                    xs[j], ys[i + 1]
                ):
                    A[u, v] = 1
                    A[v, u] = 1

    return A


def visualizar_grafo(
    B: np.ndarray,
    A: np.ndarray,
    m: int,
    n: int
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

    fig, ax = plt.subplots(figsize=(12, 12))

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

    ax.set_title("Grafo sobreposto ao labirinto")
    ax.set_xlim(-0.5, largura - 0.5)
    ax.set_ylim(altura - 0.5, -0.5)
    ax.set_aspect("equal")
    ax.set_axis_off()

    plt.tight_layout()
    plt.show()
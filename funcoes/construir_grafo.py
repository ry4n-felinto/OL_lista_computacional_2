import matplotlib.pyplot as plt
import numpy as np


def coordenadas_centros(B: np.ndarray, m: int, n: int):
    """
    Calcula as coordenadas dos centros dos vértices.
    Esta versão considera um deslocamento de meia célula
    em relação à grade anterior.
    """
    altura, largura = B.shape

    xs = [(j + 1) * largura / n - 0.5 for j in range(n)]
    ys = [(i + 1) * altura / m - 0.5 for i in range(m)]

    return xs, ys


def construir_grafo(B: np.ndarray, m: int, n: int) -> np.ndarray:
    """
    B: imagem binária (1 = corredor, 0 = parede).
    Retorna a matriz de adjacência do grafo.
    """
    if B.ndim != 2:
        raise ValueError("A imagem binária deve ser 2D.")

    if m <= 0 or n <= 0:
        raise ValueError("As dimensões da grade devem ser positivas.")

    altura, largura = B.shape
    A = np.zeros((m * n, m * n), dtype=int)
    xs, ys = coordenadas_centros(B, m, n)

    def passagem_livre(x1, y1, x2, y2):
        x1, y1 = round(x1), round(y1)
        x2, y2 = round(x2), round(y2)

        if y1 == y2:
            pixels = B[y1, min(x1, x2):max(x1, x2) + 1]
        else:
            pixels = B[min(y1, y2):max(y1, y2) + 1, x1]

        return np.all(pixels == 1)

    for i in range(m):
        for j in range(n):
            u = i * n + j

            # Vizinho à direita
            if j + 1 < n:
                if passagem_livre(xs[j], ys[i], xs[j + 1], ys[i]):
                    v = u + 1
                    A[u, v] = A[v, u] = 1

            # Vizinho abaixo
            if i + 1 < m:
                if passagem_livre(xs[j], ys[i], xs[j], ys[i + 1]):
                    v = u + n
                    A[u, v] = A[v, u] = 1

    return A


def visualizar_grafo(B: np.ndarray, A: np.ndarray, m: int, n: int):
    """
    Desenha os vértices e as arestas sobre a imagem.
    """
    if A.shape != (m * n, m * n):
        raise ValueError("Dimensão incompatível da matriz de adjacência.")

    altura, largura = B.shape
    xs, ys = coordenadas_centros(B, m, n)

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(B, cmap="gray", origin="upper", interpolation="nearest")

    for i in range(m):
        for j in range(n):
            u = i * n + j

            if j + 1 < n and A[u, u + 1] == 1:
                ax.plot(
                    [xs[j], xs[j + 1]],
                    [ys[i], ys[i]],
                    color="red",
                    linewidth=1.5,
                )

            if i + 1 < m and A[u, u + n] == 1:
                ax.plot(
                    [xs[j], xs[j]],
                    [ys[i], ys[i + 1]],
                    color="red",
                    linewidth=1.5,
                )

    for y in ys:
        for x in xs:
            ax.scatter(x, y, color="blue", s=12, zorder=3)

    ax.set_title("Grafo sobreposto ao labirinto")
    ax.set_xlim(-0.5, largura - 0.5)
    ax.set_ylim(altura - 0.5, -0.5)
    ax.set_aspect("equal")
    ax.set_axis_off()

    plt.tight_layout()
    plt.show()
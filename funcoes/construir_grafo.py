import matplotlib.pyplot as plt
import numpy as np


def construir_grafo(B: np.ndarray, m: int, n: int) -> np.ndarray:
    """
    Constrói a matriz de adjacência do grafo do labirinto.

    Args:
        B (np.ndarray): Imagem binária (1 = livre, 0 = parede).
        m (int): Número de linhas da grade.
        n (int): Número de colunas da grade.

    Returns:
        np.ndarray: Matriz de adjacência A, de dimensão (m*n, m*n).
    """

    if B.ndim != 2:
        raise ValueError("A imagem binária deve ser uma matriz 2D.")

    if m <= 0 or n <= 0:
        raise ValueError("As dimensões da grade devem ser positivas.")

    altura, largura = B.shape
    A = np.zeros((m * n, m * n), dtype=int)

    def passagem_livre(x1, y1, x2, y2):
        # Verifica os pixels entre os centros das duas células.
        x1, y1 = round(x1), round(y1)
        x2, y2 = round(x2), round(y2)

        if y1 == y2:
            pixels = B[y1, min(x1, x2) : max(x1, x2) + 1]
        else:
            pixels = B[min(y1, y2) : max(y1, y2) + 1, x1]

        return np.all(pixels == 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            u = (i - 1) * n + j - 1

            # Centro da célula em pixels.
            x = (j - 0.5) * largura / n
            y = (i - 0.5) * altura / m

            # Vizinho à direita.
            if j < n:
                x_dir = (j + 0.5) * largura / n

                if passagem_livre(x, y, x_dir, y):
                    v = u + 1
                    A[u, v] = 1
                    A[v, u] = 1

            # Vizinho abaixo.
            if i < m:
                y_baixo = (i + 0.5) * altura / m

                if passagem_livre(x, y, x, y_baixo):
                    v = u + n
                    A[u, v] = 1
                    A[v, u] = 1

    return A


def visualizar_grafo(B: np.ndarray, A: np.ndarray, m: int, n: int):
    """
    Mostra o grafo sobreposto à imagem binária do labirinto.
    B: imagem binária (1 = livre, 0 = parede).
    A: matriz de adjacência.
    m, n: número de linhas e colunas da grade.
    """

    altura, largura = B.shape

    fig, ax = plt.subplots(figsize=(10, 10))

    # Mostra o labirinto.
    ax.imshow(B, cmap="gray", origin="upper")

    # Calcula a posição dos centros das células.
    xs = [(j + 0.5) * largura / n for j in range(n)]
    ys = [(i + 0.5) * altura / m for i in range(m)]

    # Desenha as arestas.
    for u in range(m * n):
        i, j = divmod(u, n)

        for v in range(u + 1, m * n):
            if A[u, v] == 1:
                i2, j2 = divmod(v, n)

                x1, y1 = xs[j], ys[i]
                x2, y2 = xs[j2], ys[i2]

                ax.plot(
                    [x1, x2],
                    [y1, y2],
                    color="red",
                    linewidth=0.8,
                    alpha=0.8,
                )

    # Desenha os vértices.
    for y in ys:
        for x in xs:
            ax.scatter(x, y, color="blue", s=8)

    ax.set_title("Grafo sobreposto ao labirinto")
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

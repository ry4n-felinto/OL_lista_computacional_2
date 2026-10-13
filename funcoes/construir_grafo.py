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

from pathlib import Path

import numpy as np
from PIL import Image

from funcoes.construir_grafo import (
    construir_grafo,
    visualizar_grafo,
)


def carregar_labirinto(caminho: Path) -> np.ndarray:
    """
    Carrega, recorta e binariza o labirinto.

    1 = caminho livre
    0 = parede
    """
    if not caminho.exists():
        raise FileNotFoundError(
            f"Imagem não encontrada: {caminho}"
        )

    imagem = np.array(
        Image.open(caminho).convert("L")
    )

    # Localiza as margens escuras do labirinto.
    linhas, colunas = np.where(imagem < 128)

    if linhas.size == 0 or colunas.size == 0:
        raise ValueError(
            "Não foi possível localizar o labirinto na imagem."
        )

    # Recorta a margem branca externa.
    imagem = imagem[
        linhas.min():linhas.max() + 1,
        colunas.min():colunas.max() + 1
    ]

    # Binariza a imagem.
    B = (imagem > 128).astype(np.uint8)

    return B


def main():
    pasta = Path(__file__).resolve().parent
    caminho = pasta / "labirinto.jpeg"

    B = carregar_labirinto(caminho)

    m = 20
    n = 20

    print("Dimensões da imagem binária:", B.shape)
    print("Valores da imagem:", np.unique(B))

    A = construir_grafo(B, m, n)

    numero_vertices = m * n
    numero_arestas = int(np.sum(A) // 2)

    print("Número de vértices:", numero_vertices)
    print("Número de arestas:", numero_arestas)
    print("Matriz de adjacência:")
    print(A)

    visualizar_grafo(B, A, m, n)


if __name__ == "__main__":
    main()
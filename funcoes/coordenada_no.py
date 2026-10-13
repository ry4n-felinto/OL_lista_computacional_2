def coordenada_no(
    i: int,
    j: int,
    largura: int,
    altura: int,
    n: int,
    m: int
) -> tuple[float, float]:
    """
    Calcula as coordenadas em pixels do centro de uma célula.

    Args:
        i (int): Linha da célula.
        j (int): Coluna da célula.
        largura (int): Largura da imagem em pixels.
        altura (int): Altura da imagem em pixels.
        n (int): Número de colunas da grade.
        m (int): Número de linhas da grade.

    Returns:
        tuple[float, float]: Coordenadas (x, y) do centro da célula.
    """

    if largura <= 0 or altura <= 0:
        raise ValueError("As dimensões da imagem devem ser positivas.")

    if m <= 0 or n <= 0:
        raise ValueError("As dimensões da grade devem ser positivas.")

    if not (1 <= i <= m and 1 <= j <= n):
        raise ValueError("Coordenadas da célula inválidas.")

    x = (j - 0.5) * largura / n
    y = (i - 0.5) * altura / m

    return x, y
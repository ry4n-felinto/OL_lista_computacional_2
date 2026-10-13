def id_no(i: int, j: int, n: int) -> int:
    """
    Converte a posição (linha, coluna) em um identificador inteiro.

    Args:
        i (int): Linha da célula.
        j (int): Coluna da célula.
        n (int): Número de colunas da grade.

    Returns:
        int: Identificador da célula, começando em 1.
    """

    if n <= 0:
        raise ValueError("O número de colunas deve ser positivo.")

    if not (1 <= i and 1 <= j <= n):
        raise ValueError("Coordenadas inválidas.")

    return (i - 1) * n + j

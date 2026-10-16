def encontrar_extremos(matriz):
    tam_cel = matriz.shape[0] / 41

    extremos = []
    pixels = []

    for i in range(1, 21):
        ini = int(tam_cel / 2)
        fim = int(tam_cel * 40 + tam_cel / 2)
        pos = int(i * 2 * tam_cel - tam_cel / 2)

        # Superior
        if matriz[ini, pos] == 1:
            extremos.append([1, i])
            pixels.append([ini, pos])

        # Esquerda
        if matriz[pos, ini] == 1:
            extremos.append([i, 1])
            pixels.append([pos, ini])

        # Inferior
        if matriz[fim, pos] == 1:
            extremos.append([20, i])
            pixels.append([fim, pos])

        # Direita
        if matriz[pos, fim] == 1:
            extremos.append([i, 20])
            pixels.append([pos, fim])

    return extremos, pixels

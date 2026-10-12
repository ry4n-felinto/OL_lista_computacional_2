def encontrar_extremos(matriz):
    tam_cel = matriz.shape[0] / 41
    x = []

    for i in range(1, 21):
        
        ini = int(tam_cel / 2)
        fim = int(tam_cel * 40 + tam_cel / 2)
        pos = int(i  * 2 * tam_cel - tam_cel / 2)

        # Borda superior
        if matriz[ini , pos ] == 1:
           x.append([i, 1])

        # Borda esquerda
        if matriz[pos , ini] == 1:
            x.append([1, i])

        # Borda inferior
        if matriz[fim , pos] == 1:
            x.append([i, 20])

        # Borda direita
        if matriz[pos ,fim] == 1:
            x.append([20, i])

    return x
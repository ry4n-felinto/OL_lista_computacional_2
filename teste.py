from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# 1. Carrega a imagem do labirinto
pasta = Path(__file__).resolve().parent
caminho_imagem = pasta / "labirinto.jpeg"

imagem = Image.open(caminho_imagem).convert("L")
pixels = np.array(imagem)

# 2. Cria a matriz binária
B = (pixels > 127).astype(np.uint8)

print("Dimensões da imagem:", B.shape)
print("Valores encontrados:", np.unique(B))


# 3. Mostra a grade sobre o labirinto
fig, ax = plt.subplots(figsize=(12, 12))

ax.imshow(B, cmap="gray", origin="upper")

altura, largura = B.shape

for j in range(21):
    x = j * largura / 20 - 0.5
    ax.axvline(x, color="cyan", linewidth=0.7)

for i in range(21):
    y = i * altura / 20 - 0.5
    ax.axhline(y, color="cyan", linewidth=0.7)

ax.set_title("Diagnóstico: limites da grade 20 x 20")
ax.set_xlim(-0.5, largura - 0.5)
ax.set_ylim(altura - 0.5, -0.5)
ax.set_aspect("equal")
plt.tight_layout()
plt.show()

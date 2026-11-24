# Gera arte extra SEM mexer nas suas imagens: animacao de caminhada do Adam, explosao,
# sombras, telas escuras, flash de dano e cartoes. Rode: python gerar_arte_extra.py
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


def salvar(imagem, nome):
    imagem.save("assets/" + nome + ".png")


# --- Adam andando: 4 quadros por direcao (balanço do corpo, pivô nos pés)
poses = [(0, 0, 0), (0, -2, 3), (0, 1, 0), (0, -2, -3)]  # (dx, dy, angulo)
for direcao in range(8):
    base = Image.open("assets/adam_%d.png" % direcao).convert("RGBA")
    largura, altura = base.size
    for quadro, (dx, dy, angulo) in enumerate(poses):
        girada = base.rotate(angulo, resample=Image.NEAREST, center=(largura // 2, altura - 6))
        tela = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        tela.paste(girada, (dx, dy), girada)
        salvar(tela, "adam_andando_%d_%d" % (direcao, quadro))

# --- Explosao (4 quadros 64x64)
cores = [(255, 240, 150), (255, 160, 50), (230, 80, 30), (90, 90, 90)]
for quadro in range(4):
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = 10 + quadro * 7
    alpha = 255 - quadro * 55
    d.ellipse([32 - r, 32 - r, 32 + r, 32 + r], fill=cores[quadro] + (alpha,))
    if quadro < 3:
        n = r - 5
        d.ellipse([32 - n, 32 - n, 32 + n, 32 + n], fill=cores[max(0, quadro - 1)] + (alpha,))
    for ponto in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1), (1, 0), (0, 1), (-1, 0)]:
        px, py = 32 + ponto[0] * (r + 4), 32 + ponto[1] * (r + 4)
        d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=(255, 210, 90, alpha))
    salvar(im, "explosao_%d" % quadro)

# --- Sombras
for nome, w, h in [("sombra", 44, 14), ("sombra_g", 84, 24)]:
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([0, 0, w - 1, h - 1], fill=(0, 0, 0, 95))
    salvar(im.filter(ImageFilter.GaussianBlur(1.5)), nome)

# --- Telas escuras, tons de fase e flash de dano
salvar(Image.new("RGBA", (800, 560), (0, 0, 0, 170)), "overlay")
salvar(Image.new("RGBA", (800, 560), (30, 60, 100, 38)), "tom_fase2")
salvar(Image.new("RGBA", (800, 560), (80, 30, 110, 58)), "tom_fase3")
pequeno = Image.new("RGBA", (80, 56), (0, 0, 0, 0))
for x in range(80):
    for y in range(56):
        dist = max(abs(x - 40) / 40, abs(y - 28) / 28)
        pequeno.putpixel((x, y), (220, 20, 20, int(max(0, dist - 0.45) * 190)))
salvar(pequeno.resize((800, 560), Image.BICUBIC), "flash_dano")

# --- Cartao das melhorias e fundo das cenas (usa o seu menu_bg escurecido)
card = Image.new("RGBA", (380, 40), (12, 20, 26, 225))
ImageDraw.Draw(card).rectangle([0, 0, 379, 39], outline=(91, 197, 190), width=2)
salvar(card, "card")
fundo = Image.open("assets/menu_bg.png").convert("RGB").filter(ImageFilter.GaussianBlur(4))
salvar(ImageEnhance.Brightness(fundo).enhance(0.3), "cena_bg")

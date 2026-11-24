# Arte provisória da história (rode: python gerar_arte_historia.py). Troque pelos seus sprites quando quiser.
from PIL import Image, ImageDraw, ImageFilter


def salvar(imagem, nome):
    imagem.save("assets/" + nome + ".png")


def documento(cor_papel, cor_brilho, nome):
    im = Image.new("RGBA", (26, 26), (0, 0, 0, 0))
    brilho = Image.new("RGBA", (26, 26), (0, 0, 0, 0))
    ImageDraw.Draw(brilho).ellipse([1, 1, 24, 24], fill=cor_brilho + (110,))
    im.alpha_composite(brilho.filter(ImageFilter.GaussianBlur(2)))
    d = ImageDraw.Draw(im)
    d.rectangle([7, 4, 18, 21], fill=cor_papel, outline=(30, 40, 50), width=1)
    for y in (8, 11, 14, 17):
        d.line([9, y, 16, y], fill=(40, 70, 90))
    salvar(im, nome)


documento((200, 240, 250), (70, 220, 255), "pista")
documento((110, 118, 122), (60, 60, 60), "pista_lida")

# terminal
im = Image.new("RGBA", (36, 32), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.rectangle([2, 14, 33, 29], fill=(40, 46, 52), outline=(15, 18, 22), width=2)
d.rectangle([5, 3, 30, 14], fill=(30, 200, 230), outline=(180, 250, 255), width=1)
d.line([8, 7, 26, 7], fill=(10, 80, 100)); d.line([8, 10, 20, 10], fill=(10, 80, 100))
salvar(im, "terminal")

# sobrevivente
im = Image.new("RGBA", (28, 40), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.rectangle([8, 28, 12, 38], fill=(50, 40, 35)); d.rectangle([15, 28, 19, 38], fill=(50, 40, 35))
d.rounded_rectangle([5, 14, 22, 31], radius=4, fill=(120, 80, 45), outline=(60, 40, 25), width=1)
d.ellipse([8, 3, 19, 15], fill=(225, 185, 150), outline=(60, 40, 25))
d.pieslice([7, 1, 20, 13], 180, 360, fill=(90, 70, 60))
salvar(im, "sobrevivente")

# caixa de diálogo
caixa = Image.new("RGBA", (760, 130), (12, 20, 26, 232))
ImageDraw.Draw(caixa).rectangle([0, 0, 759, 129], outline=(91, 197, 190), width=2)
salvar(caixa, "caixa_dialogo")

import math

import estado
from config import W, H, WORLD_W, WORLD_H, DANO_MINIMO

state = estado.state


# ---------- texto e imagens ----------
def texto(frase, x, y, tamanho=18, cor=(232, 232, 232)):
    estado.janela.draw_text(frase, x, y, tamanho, cor)


def largura_texto(frase, tamanho):
    # largura real do texto na fonte do jogo (se a fonte não estiver disponível, estima)
    try:
        from PPlay.fontes import Fontes
        return Fontes.obter(None, tamanho).size(str(frase))[0]
    except Exception:
        return len(str(frase)) * tamanho * 0.54


def texto_centralizado(frase, y, tamanho=18, cor=(232, 232, 232), centro_x=None):
    # centraliza na tela, ou em torno de centro_x (ex.: dentro de um botão)
    if centro_x is None:
        centro_x = W / 2
    x = centro_x - largura_texto(frase, tamanho) / 2
    estado.janela.draw_text(frase, x, y, tamanho, cor)


def mostrar_mensagem(frase):
    state["mensagem"] = frase
    state["tempo_mensagem"] = 3


def desenhar_imagem_mundo(nome, x, y):
    imagem = estado.imagens[nome]
    camera = state["camera"]
    imagem.set_position(x - imagem.width / 2 - camera[0], y - imagem.height / 2 - camera[1])
    imagem.draw()


def desenhar_imagem_tela(nome, x, y):
    imagem = estado.imagens[nome]
    imagem.set_position(x, y)
    imagem.draw()


def desenhar_barras(prefixo, valor, valor_maximo, x, y, quantidade=50, arredondar_para_cima=True):
    proporcao = quantidade * valor / valor_maximo
    if arredondar_para_cima:
        cheia = math.ceil(proporcao)
    else:
        cheia = int(proporcao)
    for i in range(quantidade):
        if i < cheia:
            nome = prefixo + "c"
        else:
            nome = prefixo + "v"
        desenhar_imagem_tela(nome, x + i * 4, y)


# ---------- contas ----------
def raio(nome_da_imagem):
    # O sprite visual de Adam é maior que sua área física de colisão.
    if nome_da_imagem == "adam":
        return 12
    return estado.imagens[nome_da_imagem].width / 2 - 2


def distancia(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


def bate_no_obstaculo(x, y, raio_do_objeto):
    for bloco in state["obstaculos"]:
        dentro_x = x + raio_do_objeto > bloco["x"] and x - raio_do_objeto < bloco["x"] + bloco["w"]
        dentro_y = y + raio_do_objeto > bloco["y"] and y - raio_do_objeto < bloco["y"] + bloco["h"]
        if dentro_x and dentro_y:
            return True
    return False


def mover(objeto, dx, dy, raio_do_objeto):
    # move em x e depois em y; se bater em algo, desfaz o passo
    objeto["x"] += dx
    fora_x = objeto["x"] < raio_do_objeto or objeto["x"] > WORLD_W - raio_do_objeto
    if fora_x or bate_no_obstaculo(objeto["x"], objeto["y"], raio_do_objeto):
        objeto["x"] -= dx

    objeto["y"] += dy
    fora_y = objeto["y"] < raio_do_objeto or objeto["y"] > WORLD_H - raio_do_objeto
    if fora_y or bate_no_obstaculo(objeto["x"], objeto["y"], raio_do_objeto):
        objeto["y"] -= dy


def criar_tiro(lista, x, y, angulo, velocidade, dano, tempo_de_vida):
    lista.append({
        "x": x,
        "y": y,
        "vx": math.cos(angulo) * velocidade,
        "vy": math.sin(angulo) * velocidade,
        "tempo": tempo_de_vida,
        "dano": dano,
        "percorrido": 0,
        "alcance": velocidade * tempo_de_vida,
    })


def dano_do_tiro(tiro):
    # quanto mais longe o tiro foi, menos dano ele causa
    proporcao = min(1, tiro["percorrido"] / tiro["alcance"])
    fator = 1 - proporcao * (1 - DANO_MINIMO)
    return tiro["dano"] * fator



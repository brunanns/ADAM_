import random

import estado
from config import WORLD_W, WORLD_H, ITENS_POR_FASE
from audio import tocar_efeito
from utils import raio, distancia, bate_no_obstaculo, mostrar_mensagem
from jogador import aplicar_melhoria
from mapas import POSICOES, centro

state = estado.state


def criar_itens_da_fase():
    # cura e melhoria ficam em posições fixas do mapa da fase (ver mapas.py)
    posicoes = POSICOES[state["fase"]]
    for tipo in ("cura", "melhoria"):
        for celula in posicoes[tipo]:
            x, y = centro(celula)
            state["itens"].append({"tipo": tipo, "x": x, "y": y})


def soltar_cura(x, y):
    state["itens"].append({"tipo": "cura", "x": x, "y": y})


def atualizar_itens():
    jogador = state["jogador"]

    for item in state["itens"][:]:
        if distancia(item, jogador) < raio("adam") + 10:
            pegar_item(item)
            state["itens"].remove(item)


def pegar_item(item):
    jogador = state["jogador"]
    tocar_efeito("item")

    if item["tipo"] == "cura":
        jogador["hp"] = min(jogador["vida_max"], jogador["hp"] + 20)
    else:
        indice = random.randint(0, 3)
        nome = aplicar_melhoria(indice)
        mostrar_mensagem("Melhoria: " + nome)

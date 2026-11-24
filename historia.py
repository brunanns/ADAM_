import random

import estado
from audio import tocar_efeito
from cenas import abrir_cena
from config import WORLD_W, WORLD_H, PISTAS, SOBREVIVENTES
from mapas import POSICOES, centro
from utils import distancia, bate_no_obstaculo, mostrar_mensagem

state = estado.state

DISTANCIA_INTERACAO = 50


def posicao_livre():
    # sorteia um ponto fora dos blocos e longe de onde o Adam começa
    centro = {"x": WORLD_W / 2, "y": WORLD_H / 2}
    while True:
        ponto = {"x": random.randint(80, WORLD_W - 80), "y": random.randint(80, WORLD_H - 80)}
        if not bate_no_obstaculo(ponto["x"], ponto["y"], 20) and distancia(ponto, centro) > 150:
            return ponto


def criar_historia_da_fase():
    fase = state["fase"]

    posicoes = POSICOES[fase]

    state["pistas"] = []
    for indice, celula in enumerate(posicoes["pistas"]):
        x, y = centro(celula)
        state["pistas"].append({"tipo": "pista", "x": x, "y": y, "indice": indice, "lida": False})

    state["sobreviventes"] = []
    if SOBREVIVENTES[fase] and posicoes["sobrevivente"]:
        x, y = centro(posicoes["sobrevivente"])
        state["sobreviventes"].append({"tipo": "sobrevivente", "x": x, "y": y, "falou": False})


def atualizar_historia(dt, teclado):
    # a caixa de diálogo some sozinha depois de alguns segundos
    if state["dialogo"]:
        state["dialogo"]["tempo"] -= dt
        if state["dialogo"]["tempo"] <= 0:
            state["dialogo"] = None

    state["interagir"] = objeto_proximo()
    if state["interagir"] and teclado.key_down("e"):
        interagir(state["interagir"])


def objeto_proximo():
    jogador = state["jogador"]
    candidatos = []
    if state["terminal"]:
        candidatos.append(state["terminal"])
    for sobrevivente in state["sobreviventes"]:
        if not sobrevivente["falou"]:
            candidatos.append(sobrevivente)
    for pista in state["pistas"]:
        if not pista["lida"]:
            candidatos.append(pista)

    for objeto in candidatos:
        if distancia(objeto, jogador) < DISTANCIA_INTERACAO:
            return objeto
    return None


def interagir(objeto):
    if objeto["tipo"] == "pista":
        objeto["lida"] = True
        titulo, linhas = PISTAS[state["fase"]][objeto["indice"]]
        state["dialogo"] = {"titulo": titulo, "linhas": linhas, "tempo": 9}
        state["score"] += 50
        tocar_efeito("item")

    elif objeto["tipo"] == "sobrevivente":
        objeto["falou"] = True
        state["encontro"] = SOBREVIVENTES[state["fase"]]
        state["dialogo"] = None
        state["estado"] = "encontro"

    elif objeto["tipo"] == "terminal":
        cena = objeto["cena"]
        state["terminal"] = None
        state["fase"] += 1
        abrir_cena(cena, "iniciar_fase")


def fechar_encontro():
    jogador = state["jogador"]
    jogador["hp"] = jogador["vida_max"]
    state["score"] += 100
    state["estado"] = "jogo"
    mostrar_mensagem("Suprimentos recebidos: vida restaurada!")
